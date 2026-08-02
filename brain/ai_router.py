from brain.failover_engine import failover


def ask_ai(prompt):

    providers = failover.available()

    for provider in providers:

        try:

            print("=" * 60)
            print(f"USING {provider.upper()} AI")
            print("=" * 60)


            if provider == "groq":

                from ai.groq_client import ask
                return ask(prompt)


            elif provider == "google":

                from ai.google_client import ask
                return ask(prompt)


            elif provider == "nvidia":

                from ai.nvidia_client import ask
                return ask(prompt)


            elif provider == "openrouter":

                from ai.openrouter_client import ask
                return ask(prompt)


            elif provider == "huggingface":

                from ai.huggingface_client import ask
                return ask(prompt)


        except Exception as e:

            print(f"{provider} failed")
            print(e)

            continue


    raise Exception("All AI providers failed.")
