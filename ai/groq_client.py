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


# =====================================================
# REMOVE EMPTY KEYS
# =====================================================

GROQ_KEYS = [
    key for key in GROQ_KEYS
    if key
]


# =====================================================
# CONFIGURATION
# =====================================================

MODEL = "openai/gpt-oss-120b"


# =====================================================
# STARTUP INFORMATION
# =====================================================

print("=" * 60)
print("PROMPTPROHUB GROQ CLIENT")
print("=" * 60)

print(
    f"Groq Keys Loaded: {len(GROQ_KEYS)}"
)

print(
    f"Groq Model: {MODEL}"
)

print("=" * 60)


# =====================================================
# ASK GROQ
# =====================================================

def ask(prompt):

    # -------------------------------------------------
    # CHECK KEYS
    # -------------------------------------------------

    if not GROQ_KEYS:

        raise Exception(
            "No Groq API keys found."
        )


    last_error = None


    # -------------------------------------------------
    # ROTATE THROUGH API KEYS
    # -------------------------------------------------

    for index, api_key in enumerate(
        GROQ_KEYS,
        start=1
    ):

        try:

            print("=" * 60)
            print(
                f"Trying Groq Key {index}"
            )
            print("=" * 60)


            # -----------------------------------------
            # CREATE CLIENT
            # -----------------------------------------

            client = Groq(
                api_key=api_key
            )


            # -----------------------------------------
            # SEND REQUEST
            # -----------------------------------------

            response = (
                client.chat.completions.create(

                    model=MODEL,

                    messages=[

                        {
                            "role": "user",
                            "content": prompt
                        }

                    ]

                )
            )


            # -----------------------------------------
            # SUCCESS
            # -----------------------------------------

            print(
                f"Groq Key {index} Success"
            )


            return (
                response
                .choices[0]
                .message
                .content
            )


        except Exception as e:

            # -----------------------------------------
            # KEY FAILED
            # -----------------------------------------

            print(
                f"Groq Key {index} Failed"
            )

            print(
                str(e)
            )


            last_error = e


            # -----------------------------------------
            # TRY NEXT KEY
            # -----------------------------------------

            continue


    # =================================================
    # ALL KEYS FAILED
    # =================================================

    raise Exception(

        "All Groq API keys failed.\n"
        f"Last error: {last_error}"

)
