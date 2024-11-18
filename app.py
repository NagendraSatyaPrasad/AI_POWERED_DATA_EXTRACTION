import streamlit as st
import pandas as pd
from utils.llm_parser import parse_with_llm
import requests
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get API keys from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

# Validate API keys
if not all([GEMINI_API_KEY, GOOGLE_API_KEY, GOOGLE_CSE_ID]):
    st.error("Missing API keys. Please check your .env file.")
    st.stop()

# Function to perform a Google search
def google_search(query, api_key, cse_id):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": api_key,
        "cx": cse_id
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        if response.status_code == 400:
            st.error("Invalid API key. Please check your Google API key configuration.")
        elif response.status_code == 403:
            st.error("API quota exceeded or unauthorized. Please check your API key permissions.")
        else:
            st.error(f"Search API error: {str(e)}")
        return None

# Initialize Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Streamlit app
st.title("AI-Powered Data Extractor")

# Display API status
with st.expander("API Configuration Status"):
    st.write("Google API Key:", "✅ Configured" if GOOGLE_API_KEY else "❌ Missing")
    st.write("Google CSE ID:", "✅ Configured" if GOOGLE_CSE_ID else "❌ Missing")
    st.write("Gemini API Key:", "✅ Configured" if GEMINI_API_KEY else "❌ Missing")

# File upload section
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.write("Uploaded Data:")
    st.dataframe(data)

    # Select column for queries
    column_name = st.selectbox("Select the column to use for queries", data.columns)

    # Query input
    user_query = st.text_input(
        "Enter your query template (use {column_name} as placeholder)", 
        value=f"Find information about {{{column_name}}}"
    )

    if st.button("Run Extraction"):
        if not all([GOOGLE_API_KEY, GOOGLE_CSE_ID, GEMINI_API_KEY]):
            st.error("Please configure all required API keys in the .env file")
            st.stop()

        if column_name and user_query:
            results = []
            progress_bar = st.progress(0)
            status_text = st.empty()

            for index, entity in enumerate(data[column_name]):
                try:
                    status_text.text(f"Processing {entity}...")

                    # Format query
                    format_dict = {column_name: entity}
                    query = user_query.format(**format_dict)

                    # Perform search
                    search_results = google_search(query, GOOGLE_API_KEY, GOOGLE_CSE_ID)

                    if search_results and "items" in search_results:
                        search_text = "\n".join(
                            [item["title"] + ": " + item.get("snippet", "") 
                             for item in search_results["items"]]
                        )

                        # Use new parse_with_llm function
                        structured_data = parse_with_llm(search_text, query, GEMINI_API_KEY)
                        results.append({
                            "Entity": entity, 
                            "Structured Data": structured_data
                        })
                    else:
                        results.append({
                            "Entity": entity, 
                            "Structured Data": "No results found"
                        })

                    # Update progress
                    progress = (index + 1) / len(data[column_name])
                    progress_bar.progress(progress)

                except Exception as e:
                    st.error(f"Error processing {entity}: {str(e)}")
                    results.append({
                        "Entity": entity, 
                        "Structured Data": f"Error: {str(e)}"
                    })

            status_text.text("Processing complete!")
            
            # Display results
            st.write("Extraction Results:")
            result_df = pd.DataFrame(results)
            st.dataframe(result_df)

            # Download results
            csv = result_df.to_csv(index=False)
            st.download_button(
                "Download Results as CSV",
                data=csv,
                file_name="results.csv",
                mime="text/csv"
            )