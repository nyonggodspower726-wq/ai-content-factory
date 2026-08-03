import time


class RecoveryManager:

    def __init__(self):

        self.max_retries = 3

    def execute(self, function, *args, **kwargs):

        attempts = 0

        while attempts < self.max_retries:

            try:

                return function(*args, **kwargs)

            except Exception as e:

                attempts += 1

                print("=" * 60)
                print(f"RECOVERY ATTEMPT {attempts}")
                print(e)
                print("=" * 60)

                time.sleep(5)

        raise Exception("Maximum retries exceeded.")


recovery = RecoveryManager()
