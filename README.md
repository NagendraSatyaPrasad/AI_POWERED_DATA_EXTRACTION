# AI-Powered Data Extractor

This project is a Streamlit web application that allows users to upload a CSV file, perform automated data extraction using Google Search and Google's Generative AI (Gemini) API, and get structured insights based on the provided data. The app supports dynamic querying and structured result generation for various data entities.

## Key Features:
- Upload and visualize CSV data in the app.
- Automatically perform Google Search queries based on the data in the uploaded file.
- Extract structured information using Google's Gemini AI.
- Download the results in CSV format.
- Full integration with Google Custom Search and Gemini API.

## Requirements:

- Python 3.12+
- Streamlit
- Pandas
- Requests
- Google Generative AI (Gemini) API
- `python-dotenv` to load environment variables

## Setup

### Step 1: Install Dependencies

You can install the required dependencies using `pip`:

```bash
pip install -r requirements.txt


Create a .env file in the root of your project and add your API keys:

dotenv
Copy code
GEMINI_API_KEY=your_gemini_api_key
GOOGLE_API_KEY=your_google_api_key
GOOGLE_CSE_ID=your_google_custom_search_engine_id

To start the Streamlit app, run the following command:

bash
Copy code
streamlit run main.py

YOU CAN WATCH THE PROJECT DEMONSTRATION VIDEO HERE:
https://drive.google.com/file/d/1IOwkBIQS9nUzOU5nc95dl7yUIGj_CsbI/view?usp=sharing
