import os
import glob
import requests

from video.cache_engine import CacheEngine
from video.asset_manager import AssetManager
from video.coverr import generate_coverr_video


class ClipEngine:

    def __init__(self):

        self.assets = AssetManager()

        self.cache = CacheEngine()

        self.clip_folder = self.assets.get_clip_folder()

        print("=" * 60)
        print("PROMPTPROHUB CLIP ENGINE")
        print("=" * 60)

    def download_video(self, url, prompt):

        try:

            filename = (
                prompt.lower()
                .replace(" ", "_")
                .replace("/", "_")
            )

            filepath = os.path.join(
                self.clip_folder,
                f"{filename}.mp4"
            )

            response = requests.get(
                url,
                stream=True,
                timeout=120
            )

            response.raise_for_status()

            with open(filepath, "wb") as file:

                for chunk in response.iter_content(
                    chunk_size=1024 * 1024
                ):

                    if chunk:

                        file.write(chunk)

            return filepath

        except Exception as e:

            print("Download failed:", e)

            return None

    def generate(self, scenes):

        results = []

        if not scenes:

            return results

        available = glob.glob(

            os.path.join(

                self.clip_folder,

                "*.mp4"

            )

        )

        for scene in scenes:

            prompt = scene["prompt"]

            # --------------------------
            # CACHE
            # --------------------------

            if self.cache.exists(prompt):

                cached = self.cache.get(prompt)

                if cached and os.path.exists(cached):

                    scene["clip"] = cached

                    results.append(scene)

                    continue

            # --------------------------
            # COVERR
            # --------------------------

            print(f"Searching Coverr for: {prompt}")

            video_url = generate_coverr_video(prompt)

            if video_url:

                downloaded = self.download_video(

                    video_url,

                    prompt

                )

                if downloaded:

                    scene["clip"] = downloaded

                    self.cache.save(

                        prompt,

                        downloaded

                    )

                    results.append(scene)

                    continue

            # --------------------------
            # LOCAL FALLBACK
            # --------------------------

            if available:

                clip = available[
                    len(results) % len(available)
                ]

                scene["clip"] = clip

            else:

                scene["clip"] = None

                print(
                    f"No clip found for '{prompt}'"
                )

            results.append(scene)

        print(f"{len(results)} clips prepared.")

        return results
