import google.generativeai as genai
import sys
import os
from dotenv import load_dotenv

try:
    # Load API key from environment variable
    load_dotenv()  # This loads environment variables from a .env file
    api_key = os.getenv('')
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    
    # Let's make the prompt more specific
    response = model.generate_content('Write a simple java hello world program')
    print(response.text)

finally:
    sys.exit(0)