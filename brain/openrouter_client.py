import os

from openai import OpenAI


client = OpenAI(

    base_url="https://openrouter.ai/api/v1",

    api_key=os.getenv("OPENROUTER_API_KEY")

)


def ask(prompt):

    response = client.chat.completions.create(

        model="deepseek/deepseek-chat-v3-0324",

        messages=[

            {
                "role": "system",
                "content": "You are PromptProHub AI Studio. Produce high-quality marketing, business, and digital product content."
            },

            {
                "role": "user",
                "content": prompt
            }

        ],

        temperature=0.7,

        max_tokens=2048

    )

    return response.choices[0].message.content
