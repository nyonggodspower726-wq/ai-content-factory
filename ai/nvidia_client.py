import os
from openai import OpenAI

MODEL = "meta/llama-3.3-70b-instruct"

API_KEYS = [

    os.getenv("NVIDIA_API_KEY_1"),

    os.getenv("NVIDIA_API_KEY_2"),

    os.getenv("NVIDIA_API_KEY_3")

]

API_KEYS = [k for k in API_KEYS if k]


def ask(prompt):

    last_error = None

    for index, api_key in enumerate(API_KEYS, start=1):

        try:

            print("=" * 60)
            print(f"USING NVIDIA KEY {index}")
            print("=" * 60)

            client = OpenAI(
                base_url="https://integrate.api.nvidia.com/v1",
                api_key=api_key,
                timeout=120
            )

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

            print(f"NVIDIA KEY {index} SUCCESS")

            return response.choices[0].message.content

        except Exception as e:

            print("=" * 60)
            print(f"NVIDIA KEY {index} FAILED")
            print("=" * 60)
            print(e)

            last_error = e

            continue

    raise last_error if last_error else Exception("No NVIDIA API keys configured.")
