import os
from openai import OpenAI

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY"),
    timeout=120
)

MODEL = "meta/llama-3.3-70b-instruct"


def ask(prompt):

    try:

        response = client.chat.completions.create(

            model=MODEL,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.7,

            max_tokens=2048

        )

        return response.choices[0].message.content

    except Exception as e:

        print("=" * 60)
        print("NVIDIA ERROR")
        print("=" * 60)
        print(e)
        raise
