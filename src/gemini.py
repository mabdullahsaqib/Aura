import google.generativeai as genai
import os

genai.configure(api_key="")

model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(
    history=[
        {"role": "user", "parts": "I have 2 dogs in my house."},
        {"role": "model", "parts": "That's wonderful! Two dogs mean twice the love and twice the fun.  😊  What breeds are they? Are they good friends? Do they have any funny quirks? 🐶"},
    ]
)
response = chat.send_message("How many paws are in my house?")
print(response.text)