import os
from groq import Groq

api_key = os.getenv("GROQ_API_KEY")

print("=" * 60)
print("GROQ CLIENT")
print("=" * 60)
print("API Key Loaded:", bool(api_key))
print("=" * 60)

client = Groq(
    api_key=api_key
)


def ask(prompt):

    print("Calling Groq...")

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]

    )

    print("Groq Success")

    return response.choices[0].message.content
