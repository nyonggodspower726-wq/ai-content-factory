import os
from openai import OpenAI


client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)


def ask(prompt):

    response = client.chat.completions.create(

        model="meta/llama-3.3-70b-instruct",

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
