from brain.provider_memory import provider_memory


def ask_ai(prompt):

    # ==========================================
    # Try last successful provider first
    # ==========================================

    remembered = provider_memory.best_provider()

    if remembered:

        try:

            print("=" * 60)
            print(f"USING SAVED {remembered.upper()} AI")
            print("=" * 60)

            if remembered == "groq":

                from ai.groq_client import ask

                return ask(prompt)

            elif remembered == "nvidia":

                from ai.nvidia_client import ask

                return ask(prompt)

        except Exception as e:

            print(f"{remembered} failed")
            print(e)

            provider_memory.clear()

    # ==========================================
    # Provider Priority
    # ==========================================

    providers = [

        "groq",
        "nvidia"

    ]

    # ==========================================
    # Try Providers
    # ==========================================

    for provider in providers:

        try:

            print("=" * 60)
            print(f"USING {provider.upper()} AI")
            print("=" * 60)

            if provider == "groq":

                from ai.groq_client import ask

                result = ask(prompt)

            elif provider == "nvidia":

                from ai.nvidia_client import ask

                result = ask(prompt)

            else:

                continue

            provider_memory.remember(provider)
            provider_memory.success(provider)

            return result

        except Exception as e:

            print(f"{provider} failed")
            print(e)

            provider_memory.remember(provider)
            provider_memory.failed(provider)

            continue

    raise Exception("All AI providers failed.")
