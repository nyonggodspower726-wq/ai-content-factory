from brain.pipeline import pipeline
from brain.script_engine import generate_script
from brain.voice_engine import generate_voice as create_voice_profile
from brain.cta_engine import choose_cta
from video.voice_generator import generate_voice as create_audio


class ProductionManager:

    def __init__(self):
        print("=" * 60)
        print("PROMPTPROHUB AI STUDIO BRAIN ONLINE")
        print("=" * 60)

    def produce(self, topic, platform="tiktok", video_number=1):

        print("=" * 60)
        print("PROMPTPROHUB AI PRODUCTION MANAGER")
        print("=" * 60)
        print(f"Campaign Topic: {topic}")
        print(f"Platform: {platform.upper()}")
        print(f"Video Number: {video_number}/4")
        print("=" * 60)

        try:

            print("Running AI Strategy Pipeline...")

            project = pipeline.run(topic)

            if not project:
                print("Pipeline returned nothing.")
                return None

            if isinstance(project, dict):
                project["platform"] = platform
                project["video_number"] = video_number

            # =====================================================
            # SCRIPT
            # =====================================================

            print("Generating Script...")

            script = generate_script(project)

            # =====================================================
            # CTA
            # =====================================================

            print("Generating Conversion CTA...")

            cta = choose_cta(topic)

            if not cta:
                cta = (
                    "If you want to use AI to work smarter, "
                    "click the link in bio to explore PromptProHub, "
                    "and follow for more AI tools and strategies."
                )

            print("=" * 60)
            print("SELECTED CTA")
            print("=" * 60)
            print(cta)
            print("=" * 60)

            # =====================================================
            # ADD CTA TO SCRIPT
            # =====================================================

            if isinstance(script, dict):

                existing_script = script.get(
                    "script",
                    ""
                )

                if not existing_script:
                    existing_script = str(script)

                script["cta"] = cta
                script["platform"] = platform
                script["video_number"] = video_number

                script["script"] = (
                    existing_script.strip()
                    + "\n\n"
                    + cta
                )

            else:

                script = (
                    str(script).strip()
                    + "\n\n"
                    + cta
                )

            print("CTA successfully added to script.")

            # =====================================================
            # VOICE PROFILE
            # =====================================================

            print("Generating Voice Profile...")

            voice_profile = create_voice_profile(
                project
            )

            # =====================================================
            # AI VOICE
            # =====================================================

            print("Generating AI Voice...")

            voice_file = create_audio(
                script,
                voice_profile
            )

            # =====================================================
            # PRODUCTION RESULT
            # =====================================================

            result = {
                "topic": topic,
                "platform": platform,
                "video_number": video_number,
                "project": project,
                "script": script,
                "cta": cta,
                "voice_profile": voice_profile,
                "voice": voice_file,
                "status": "READY FOR VIDEO"
            }

            print("=" * 60)
            print("PRODUCTION PLAN READY")
            print("=" * 60)
            print(f"Platform: {platform.upper()}")
            print(f"Video: {video_number}/4")
            print("CTA INCLUDED:", cta)
            print("=" * 60)

            return result

        except Exception as e:

            print("=" * 60)
            print("PRODUCTION MANAGER FAILED")
            print("=" * 60)
            print("ERROR TYPE:", type(e).__name__)
            print("ERROR:", str(e))
            print("=" * 60)

            return None


production = ProductionManager()
