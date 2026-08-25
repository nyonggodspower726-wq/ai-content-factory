import os
from openai import OpenAI


# =====================================================
# PROMPTPROHUB NVIDIA CLIENT
# Automatic API Key Rotation
# =====================================================

MODEL = "nvidia/llama-3.3-nemotron-super-49b-v1.5"

API_KEYS = [
    os.getenv("NVIDIA_API_KEY_1"),
    os.getenv("NVIDIA_API_KEY_2"),
    os.getenv("NVIDIA_API_KEY_3")
]

# Remove empty keys
API_KEYS = [
    key for key in API_KEYS
    if key
]


print("=" * 60)
print("PROMPTPROHUB NVIDIA CLIENT")
print("=" * 60)
print(f"NVIDIA Keys Loaded: {len(API_KEYS)}")
print(f"NVIDIA Model: {MODEL}")
print("NVIDIA Endpoint: https://integrate.api.nvidia.com/v1")
print("=" * 60)


# =====================================================
# ASK NVIDIA
# =====================================================

def ask(prompt):

    if not API_KEYS:
        raise Exception(
            "No NVIDIA API keys configured."
        )

    last_error = None


    # =================================================
    # TRY EVERY NVIDIA KEY
    # =================================================

    for index, api_key in enumerate(
        API_KEYS,
        start=1
    ):

        try:

            print("=" * 60)
            print(f"USING NVIDIA KEY {index}")
            print("=" * 60)


            client = OpenAI(

                base_url=(
                    "https://integrate.api.nvidia.com/v1"
                ),

                api_key=api_key,

                timeout=300.0,

                max_retries=0

            )


            response = (
                client.chat.completions.create(

                    model=MODEL,

                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],

                    temperature=0.7,

                    max_tokens=2048,

                    stream=False

                )
            )


            # =================================================
            # SUCCESS
            # =================================================

            result = (
                response
                .choices[0]
                .message
                .content
            )


            if not result:

                raise Exception(
                    "NVIDIA returned an empty response."
                )


            print("=" * 60)
            print(f"NVIDIA KEY {index} SUCCESS")
            print("=" * 60)


            return result


        except Exception as e:

            print("=" * 60)
            print(f"NVIDIA KEY {index} FAILED")
            print("=" * 60)

            print(
                "ERROR TYPE:",
                type(e).__name__
            )

            print(
                "ERROR:",
                str(e)
            )

            print("=" * 60)


            last_error = e

            continue


    # =================================================
    # ALL NVIDIA KEYS FAILED
    # =================================================

    raise Exception(
        "All NVIDIA API keys failed.\n"
        f"Last error: {last_error}"
        )
