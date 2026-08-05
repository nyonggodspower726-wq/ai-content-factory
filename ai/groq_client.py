import os
from groq import Groq

# =====================================================
# PROMPTPROHUB GROQ CLIENT
# Automatic API Key Rotation
# =====================================================

GROQ_KEYS = [

    os.getenv("GROQ_API_KEY_1"),

    os.getenv("GROQ_API_KEY_2")

]

# Remove empty keys
GROQ_KEYS = [key for key in GROQ_KEYS if key]

print("=" * 60)
print("PROMPTPROHUB GROQ CLIENT")
print("=" * 60)
print(f"Groq Keys Loaded: {len(GROQ_KEYS)}")
print("=" * 60)


MODEL = "llama-3.3-70b-versatile"


def ask(prompt):

    if not GROQ_KEYS:

        raise Exception("No Groq API keys found.")

    last_error = None

    for index, api_key in enumerate(GROQ_KEYS, start=1):

        try:

            print("=" * 60)
            print(f"Trying Groq Key {index}")
            print("=" * 60)

            client = Groq(
                api_key=api_key
            )

            response = client.chat.completions.create(

                model=MODEL,

                messages=[

                    {
                        "role": "user",
                        "content": prompt
                    }

                ]

            )

            print(f"Groq Key {index} Success")

            return response.choices[0].message.content

        except Exception as e:

            print(f"Groq Key {index} Failed")
            print(e)

            last_error = e

            continue

    raise Exception(
        f"All Groq API keys failed.\n{last_error}"
        )
