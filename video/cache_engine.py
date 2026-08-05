import os
import json
import hashlib


class CacheEngine:

    def __init__(self):

        self.cache_folder = "assets/cache"

        self.cache_file = os.path.join(
            self.cache_folder,
            "cache.json"
        )

        os.makedirs(
            self.cache_folder,
            exist_ok=True
        )

        if not os.path.exists(self.cache_file):

            with open(self.cache_file, "w") as file:

                json.dump({}, file)

        print("=" * 60)
        print("CACHE ENGINE READY")
        print("=" * 60)

    def _load_cache(self):

        with open(self.cache_file, "r") as file:

            return json.load(file)

    def _save_cache(self, cache):

        with open(self.cache_file, "w") as file:

            json.dump(
                cache,
                file,
                indent=4
            )

    def generate_key(self, prompt):

        return hashlib.md5(

            prompt.encode()

        ).hexdigest()

    def exists(self, prompt):

        cache = self._load_cache()

        key = self.generate_key(prompt)

        return key in cache

    def get(self, prompt):

        cache = self._load_cache()

        key = self.generate_key(prompt)

        return cache.get(key)

    def save(

        self,

        prompt,

        file_path

    ):

        cache = self._load_cache()

        key = self.generate_key(prompt)

        cache[key] = file_path

        self._save_cache(cache)

        print(

            f"Cached: {file_path}"

        )

    def clear(self):

        self._save_cache({})

        print("Cache cleared.")
