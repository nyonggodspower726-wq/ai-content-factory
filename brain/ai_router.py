from brain.failover_engine import failover
from brain.provider_memory import provider_memory


def ask_ai(prompt):

    # Try the last successful provider first
    remembered = provider_memory.get()

    if remembered:

        try:

            print("=" * 60)
            print(f"USING SAVED {remembered.upper()} AI")
            print("=" * 60)

            if remembered == "groq":
                from ai.groq_client import ask
                return ask(prompt)

            elif remembered == "google":
                from ai.google_client import ask
                return ask(prompt)

            elif remembered == "nvidia":
                from ai.nvidia_client import ask
                return ask(prompt)

            elif remembered == "openrouter":
                from ai.openrouter_client import ask
                return ask(prompt)

        except Exception as e:

            print(f"{remembered} failed")
            print(e)

            provider_memory.clear()


    # If no saved provider or it failed, try all providers
    providers = failover.available()

    for provider in providers:

        try:

            print("=" * 60)
            print(f"USING {provider.upper()} AI")
            print("=" * 60)

            if provider == "groq":

                from ai.groq_client import ask
                result = ask(prompt)

            elif provider == "google":

                from ai.google_client import ask
                result = ask(prompt)

            elif provider == "nvidia":

                from ai.nvidia_client import ask
                result = ask(prompt)

            elif provider == "openrouter":

                from ai.openrouter_client import ask
                result = ask(prompt)

            else:
                continue

            # Remember the working provider
            provider_memory.set(provider)

            return result

        except Exception as e:

            print(f"{provider} failed")
            print(e)

            continue

    raise Exception("All AI providers failed.")
