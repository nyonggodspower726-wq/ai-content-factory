import os
import glob

from video.cache_engine import CacheEngine
from video.asset_manager import AssetManager


class ClipEngine:

    def __init__(self):

        self.assets = AssetManager()

        self.cache = CacheEngine()

        self.clip_folder = self.assets.get_clip_folder()

        print("=" * 60)
        print("PROMPTPROHUB CLIP ENGINE")
        print("=" * 60)

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

        if len(available) == 0:

            print("No local clips found.")

        for scene in scenes:

            prompt = scene["prompt"]

            # Cache lookup
            if self.cache.exists(prompt):

                cached = self.cache.get(prompt)

                if cached and os.path.exists(cached):

                    scene["clip"] = cached

                    results.append(scene)

                    continue

            # Local clip fallback
            if available:

                clip = available[
                    len(results) % len(available)
                ]

                scene["clip"] = clip

                self.cache.save(

                    prompt,

                    clip

                )

            else:

                scene["clip"] = None

            results.append(scene)

        print(f"{len(results)} clips prepared.")

        return results
