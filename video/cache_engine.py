import os
import requests

from video.cache_engine import CacheEngine
from video.coverr import generate_coverr_video


class ClipEngine:

    def __init__(self):

        self.cache = CacheEngine()

        self.clip_folder = "assets/clips"

        os.makedirs(
            self.clip_folder,
            exist_ok=True
        )

        print("=" * 60)
        print("PROMPTPROHUB CLIP ENGINE")
        print("=" * 60)


    def download_clip(

        self,

        url,

        filename

    ):

        try:

            print(
                "Downloading clip..."
            )

            response = requests.get(

                url,

                stream=True,

                timeout=180

            )

            response.raise_for_status()


            with open(

                filename,

                "wb"

            ) as file:


                for chunk in response.iter_content(

                    chunk_size=1024 * 1024

                ):

                    if chunk:

                        file.write(chunk)



            print(
                f"Saved: {filename}"
            )


            return filename



        except Exception as e:

            print(
                f"Download failed: {e}"
            )

            return None



    def generate(self, scenes):


        results = []


        if not scenes:

            return results



        for index, scene in enumerate(scenes):


            prompt = scene.get(

                "prompt",

                ""

            )


            if not prompt:

                continue



            print("=" * 60)

            print(
                f"Processing Scene {index + 1}"
            )

            print(
                f"Prompt: {prompt}"
            )

            print("=" * 60)



            # ---------------------------------
            # CHECK CACHE FIRST
            # ---------------------------------

            if self.cache.exists(prompt):

                cached = self.cache.get(prompt)


                if cached and os.path.exists(cached):

                    print(
                        "Using cached clip."
                    )

                    scene["clip"] = cached

                    results.append(scene)

                    continue



            # ---------------------------------
            # SEARCH COVERR
            # ---------------------------------

            video_url = generate_coverr_video(

                prompt

            )


            if not video_url:

                print(
                    "No clip found from Coverr."
                )

                scene["clip"] = None

                results.append(scene)

                continue



            # ---------------------------------
            # DOWNLOAD CLIP
            # ---------------------------------

            filename = os.path.join(

                self.clip_folder,

                f"scene_{index + 1}.mp4"

            )


            clip_file = self.download_clip(

                video_url,

                filename

            )


            if clip_file:


                scene["clip"] = clip_file


                self.cache.save(

                    prompt,

                    clip_file

                )


            else:

                scene["clip"] = None



            results.append(scene)



        print("=" * 60)

        print(
            f"{len(results)} clips prepared."
        )

        print("=" * 60)


        return results
