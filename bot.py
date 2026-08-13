import os
import traceback
from brain.production_manager import production
from brain.seo_engine import generate_seo
from brain.trend_brain import choose_trending_topic
from brain.viral_angle_engine import choose_best_angle
from brain.curiosity_engine import choose_curiosity
from brain.hook_engine import choose_hook
from brain.retention_engine import choose_retention
from video.video_generator import create_video
from social.status200_publisher import publish_to_status200
from social.instagram_zernio import publish_to_instagram
from social.youtube_shorts import upload_to_youtube
from file_manager import save_text
from logger import log

PLATFORM_CONFIG = {
    "tiktok": {
        "label": "TIKTOK",
        "music": True
    },
    "instagram": {
        "label": "INSTAGRAM",
        "music": True
    },
    "youtube": {
        "label": "YOUTUBE",
        "music": False
    }
}

def main(topic=None, platform="tiktok", video_number=1):
    print("=" * 60)
    print("PROMPTPROHUB AI STUDIO ONLINE")
    print("=" * 60)
    print(f"PLATFORM: {platform.upper()}")
    print(f"VIDEO NUMBER: {video_number}")
    print("=" * 60)
    if platform not in PLATFORM_CONFIG:
        raise ValueError(f"Unsupported platform: {platform}")
    try:
        config = PLATFORM_CONFIG[platform]
        if topic is None:
            topic = choose_trending_topic()
        log(f"Selected Viral Topic: {topic}")
        angle = choose_best_angle(topic)
        curiosity = choose_curiosity(topic)
        hook = choose_hook(topic, angle, curiosity)
        retention = choose_retention(topic)
        creative_data = {
            "topic": topic,
            "platform": platform,
            "video_number": video_number,
            "angle": angle,
            "curiosity": curiosity,
            "hook": hook,
            "retention": retention
        }
        save_text(
            f"creative_brain_{platform}_{video_number}.json",
            creative_data
        )
        log(f"Hook: {hook}")
        log(f"Curiosity: {curiosity}")
        log(f"Retention: {retention}")
        log(f"Starting {platform} production #{video_number}")
        production_plan = production.produce(
            topic,
            platform=platform,
            video_number=video_number
        )
        if not production_plan:
            log("Production brain returned nothing.")
            return None
        project = production_plan.get("project", {})
        script = production_plan.get("script", {})
        voice_file = production_plan.get("voice")
        save_text(
            f"script_{platform}_{video_number}.json",
            script
        )
        save_text(
            f"voice_{platform}_{video_number}.json",
            production_plan.get("voice_profile", {})
        )
        log("Generating platform-specific SEO...")
        seo = generate_seo(topic)
        save_text(
            f"seo_{platform}_{video_number}.json",
            seo
        )
        scene_prompts = project.get(
            "scene_prompts",
            []
        )
        if not scene_prompts:
            log("No scene prompts available.")
            return None
        print("=" * 60)
        print("VIDEO GENERATION")
        print("=" * 60)
        print(f"Platform: {platform}")
        print(f"Video: {video_number}/4")
        print(f"Scenes: {len(scene_prompts)}")
        print(f"YouTube Music Disabled: {not config['music']}")
        print("=" * 60)
        video = create_video(
            scene_prompts,
            script,
            voice_file,
            platform=platform,
            video_number=video_number,
            music_enabled=config["music"]
        )
        if not video:
            log("Video generation failed.")
            return None
        if not os.path.exists(video):
            log(f"Rendered video not found: {video}")
            return None
        print("=" * 60)
        print("VIDEO CREATED SUCCESSFULLY")
        print(video)
        print("=" * 60)
        caption = hook
        if platform == "tiktok":
            try:
                log("Publishing TikTok video...")
                result = publish_to_status200(
                    video,
                    caption,
                    platform="tiktok",
                    video_number=video_number
                )
                print("TikTok result:", result)
            except Exception as e:
                log(f"TikTok publishing failed: {e}")
                traceback.print_exc()
        elif platform == "instagram":
            try:
                log("Publishing Instagram Reel through Zernio...")
                result = publish_to_instagram(
                    video,
                    caption
                )
                print("Instagram result:", result)
            except Exception as e:
                log(f"Instagram publishing failed: {e}")
                traceback.print_exc()
        elif platform == "youtube":
            try:
                log("Uploading YouTube Short...")
                if isinstance(seo, dict):
                    youtube_title = seo.get(
                        "click_title",
                        seo.get(
                            "title",
                            topic
                        )
                    )
                    youtube_description = seo.get(
                        "description",
                        ""
                    )
                else:
                    youtube_title = topic
                    youtube_description = str(seo)
                thumbnail_path = (
                    "assets/hook_images/"
                    "promptprohub_hook.jpg"
                )
                if not os.path.exists(thumbnail_path):
                    thumbnail_path = None
                upload_to_youtube(
                    video,
                    youtube_title,
                    youtube_description,
                    thumbnail_path
                )
                log("YouTube upload completed.")
            except Exception as e:
                log(f"YouTube upload failed: {e}")
                traceback.print_exc()
        print("=" * 60)
        print("PLATFORM PRODUCTION COMPLETE")
        print("=" * 60)
        print(f"Platform: {platform}")
        print(f"Video Number: {video_number}")
        print(f"Video: {video}")
        print("=" * 60)
        return {
            "success": True,
            "platform": platform,
            "video_number": video_number,
            "topic": topic,
            "video": video,
            "hook": hook,
            "seo": seo
        }
    except Exception as e:
        print("=" * 60)
        print("BOT FAILED")
        print("=" * 60)
        print(f"ERROR TYPE: {type(e).__name__}")
        print(f"ERROR: {repr(e)}")
        traceback.print_exc()
        log(
            f"BOT FAILED: "
            f"{type(e).__name__}: {e}"
        )
        return None

if __name__ == "__main__":
    main()
