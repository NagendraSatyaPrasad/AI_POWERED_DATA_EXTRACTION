# utils/llm_parser.py
import google.generativeai as genai

def parse_with_llm(search_results, query, gemini_api_key):
    """
    Parses search results using Google's Generative AI (Gemini) API.
    
    Args:
        search_results (str): The search results to parse
        query (str): The original query
        gemini_api_key (str): The Gemini API key
    
    Returns:
        str: Structured data extracted from the search results
    """
    try:
        # Configure the Gemini API
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        # Construct the prompt
        prompt = f"""
        Based on the following search results and query, extract relevant structured information:
        
        Query: {query}
        
        Search Results:
        {search_results}
        
        Please provide the extracted information in a clear, structured format.
        """
        
        # Generate response
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"Error in parsing: {str(e)}"