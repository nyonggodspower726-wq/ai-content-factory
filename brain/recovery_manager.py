import time


class RecoveryManager:

    def __init__(self):

        self.max_retries = 3

        self.retry_delay = 5

        self.failed_engines = []


    def execute(self, function, *args, **kwargs):

        attempts = 0

        last_error = None

        while attempts < self.max_retries:

            try:

                return function(*args, **kwargs)

            except Exception as e:

                attempts += 1

                last_error = e

                print("=" * 60)
                print(f"RECOVERY ATTEMPT {attempts}/{self.max_retries}")
                print(f"FUNCTION : {function.__name__}")
                print(f"ERROR    : {e}")
                print("=" * 60)

                time.sleep(self.retry_delay)

        self.failed_engines.append({

            "engine": function.__name__,

            "error": str(last_error)

        })

        raise Exception(

            f"{function.__name__} failed after "
            f"{self.max_retries} retries."

        )


    def report(self):

        print("=" * 60)
        print("RECOVERY REPORT")
        print("=" * 60)

        if not self.failed_engines:

            print("No failed engines.")

        else:

            for item in self.failed_engines:

                print(
                    f"{item['engine']} -> {item['error']}"
                )

        print("=" * 60)


    def reset(self):

        self.failed_engines = []


recovery = RecoveryManager()
