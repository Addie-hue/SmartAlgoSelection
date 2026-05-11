import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

print(f"Using key: {api_key[:10]}...{api_key[-5:]}")

genai.configure(api_key=api_key)

try:
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Say hello")
    print("Success!")
    print(response.text)
except Exception as e:
    print(f"Error: {e}")
