import os
import google.generativeai as genai

genai.configure(
    api_key=os.getenv("GOOGLE_API_KEY")
)

# Create Gemini model
model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def ask(prompt):

    response = model.generate_content(prompt)

    return response.text
