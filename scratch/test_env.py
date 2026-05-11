import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GEMINI_API_KEY")

if key:
    print(f"Key found! Length: {len(key)}")
    print(f"Prefix: {key[:7]}...")
else:
    print("Key NOT found in environment.")
