import google.generativeai as genai
from config import GEMINI_API_KEY


# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

genai.configure(api_key= GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat()

response = chat.send_message()
print(response)
print(response.text)