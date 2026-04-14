import os
from dotenv import load_dotenv
import google.generativeai as genai
load_dotenv(override=True) 
my_key = os.getenv("GOOGLE_API_KEY") 
print(os.getenv("GOOGLE_API_KEY"))
genai.configure(api_key=my_key)
model = genai.GenerativeModel('gemini-2.5-flash')