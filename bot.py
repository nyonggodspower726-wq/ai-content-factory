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

============================================================

SOCIAL PUBLISHERS

============================================================

STATUS 200:

TikTok #1

LinkedIn

TikTok #2

Pinterest

from social.status200_publisher import publish_to_status200

ZERNIO:

Instagram @promptprohub3

from social.instagram_zernio import publish_to_instagram

YOUTUBE:

from social.youtube_shorts import upload_to_youtube

from file_manager import save_text
from logger import log

============================================================

MAIN

============================================================

def main(topic=None):

print("=" * 60)  
print("PROMPTPROHUB AI STUDIO ONLINE")  
print("=" * 60)  

try:  

    # =====================================================  
    # CREATIVE BRAIN  
    # =====================================================  

    log(  
        "ACTIVATING NEW CONTENT BRAIN..."  
    )  

    log(  
        "Running Trend Intelligence Engine..."  
    )  

    if topic is None:  

        topic = choose_trending_topic()  

    log(  
        f"Selected Viral Topic: {topic}"  
    )  

    # =====================================================  
    # VIRAL ANGLE  
    # =====================================================  

    angle = choose_best_angle(  
        topic  
    )  

    # =====================================================  
    # CURIOSITY  
    # =====================================================  

    curiosity = choose_curiosity(  
        topic  
    )  

    # =====================================================  
    # HOOK  
    # =====================================================  

    hook = choose_hook(  
        topic,  
        angle,  
        curiosity  
    )  

    # =====================================================  
    # RETENTION  
    # =====================================================  

    retention = choose_retention(  
        topic  
    )  

    # =====================================================  
    # SAVE CREATIVE BRAIN  
    # =====================================================  

    save_text(  
        "creative_brain.json",  
        {  
            "topic": topic,  
            "angle": angle,  
            "curiosity": curiosity,  
            "hook": hook,  
            "retention": retention  
        }  
    )  

    log(  
        f"Selected Topic: {topic}"  
    )  

    log(  
        f"Hook: {hook}"  
    )  

    log(  
        f"Curiosity: {curiosity}"  
    )  

    log(  
        f"Retention: {retention}"  
    )  

    # =====================================================  
    # PRODUCTION  
    # =====================================================  

    log(  
        f"Starting campaign: {topic}"  
    )  

    log(  
        "Running AI production brain..."  
    )  

    production_plan = production.produce(  
        topic  
    )  

    if not production_plan:  

        log(  
            "Production brain returned nothing"  
        )  

        return  

    project = production_plan.get(  
        "project",  
        {}  
    )  

    script = production_plan.get(  
        "script",  
        {}  
    )  

    voice_file = production_plan.get(  
        "voice"  
    )  

    # =====================================================  
    # SAVE SCRIPT  
    # =====================================================  

    save_text(  
        "script.json",  
        script  
    )  

    save_text(  
        "voice.json",  
        production_plan.get(  
            "voice_profile",  
            {}  
        )  
    )  

    # =====================================================  
    # SEO  
    # =====================================================  

    log(  
        "Generating SEO..."  
    )  

    seo = generate_seo(  
        topic  
    )  

    save_text(  
        "seo.json",  
        seo  
    )  

    # =====================================================  
    # DEBUG  
    # =====================================================  

    print("=" * 60)  
    print("DEBUG INFORMATION")  
    print("=" * 60)  

    scene_prompts = project.get(  
        "scene_prompts",  
        []  
    )  

    print(  
        "Voice File:",  
        voice_file  
    )  

    print(  
        "Voice Exists:",  
        bool(  
            voice_file  
            and os.path.exists(  
                voice_file  
            )  
        )  
    )  

    print(  
        "Scene Prompts:",  
        len(scene_prompts)  
    )  

    if scene_prompts:  

        print(  
            "First Scene:",  
            scene_prompts[0]  
        )  

    if isinstance(  
        script,  
        dict  
    ):  

        print(  
            "Script Keys:",  
            list(  
                script.keys()  
            )  
        )  

    else:  

        print(  
            "Script Type:",  
            type(script)  
        )  

    print("=" * 60)  

    # =====================================================  
    # VIDEO GENERATION  
    # =====================================================  

    log(  
        "Rendering AI sales video..."  
    )  

    video = create_video(  
        scene_prompts,  
        script,  
        voice_file  
    )  

    if not video:  

        log(  
            "Video generation failed."  
        )  

        return  

    if not os.path.exists(  
        video  
    ):  

        log(  
            f"Rendered video not found: {video}"  
        )  

        return  

    print("=" * 60)  
    print("VIDEO CREATED SUCCESSFULLY")  
    print(video)  
    print("=" * 60)  

    # =====================================================  
    # CAPTION  
    # =====================================================  

    caption = hook  

    # =====================================================  
    # STATUS 200  
    #  
    # Account 1 = TikTok  
    # Account 2 = LinkedIn  
    # Account 3 = TikTok 2  
    # Account 4 = Pinterest  
    #  
    # status200_publisher.py handles the accounts  
    # sequentially and continues if one fails.  
    # =====================================================  

    try:  

        log(  
            "Publishing to Status 200 accounts..."  
        )  

        status200_result = (  
            publish_to_status200(  
                video,  
                caption  
            )  
        )  

        print("=" * 60)  
        print(  
            "STATUS 200 MULTI-ACCOUNT RESULT"  
        )  
        print("=" * 60)  

        print(  
            status200_result  
        )  

        log(  
            "Status 200 publishing finished."  
        )  

    except Exception as e:  

        print("=" * 60)  
        print(  
            "STATUS 200 PUBLISHING FAILED"  
        )  
        print("=" * 60)  

        print(  
            "Error:",  
            e  
        )  

        print(  
            "Status 200 traceback:"  
        )  

        traceback.print_exc()  

        log(  
            f"Status 200 publishing failed: {e}"  
        )  

    # =====================================================  
    # INSTAGRAM — ZERNIO  
    #  
    # Connected Instagram:  
    # @promptprohub3  
    #  
    # IMPORTANT:  
    # The Zernio uploader receives the LOCAL video path.  
    # It uploads the MP4 to Zernio and then publishes  
    # the Instagram Reel.  
    # =====================================================  

    try:  

        log(  
            "Publishing Instagram Reel through Zernio..."  
        )  

        instagram_result = (  
            publish_to_instagram(  
                video,  
                caption  
            )  
        )  

        print("=" * 60)  
        print(  
            "INSTAGRAM REEL PUBLISH SUCCESS"  
        )  
        print("=" * 60)  

        print(  
            "Instagram:",  
            "@promptprohub3"  
        )  

        print(  
            "Zernio Result:",  
            instagram_result  
        )  

        print("=" * 60)  

        log(  
            "Instagram Reel publishing completed."  
        )  

    except Exception as e:  

        print("=" * 60)  
        print(  
            "INSTAGRAM REEL PUBLISH FAILED"  
        )  
        print("=" * 60)  

        print(  
            "Instagram:",  
            "@promptprohub3"  
        )  

        print(  
            "Error:",  
            e  
        )  

        print(  
            "Instagram traceback:"  
        )  

        traceback.print_exc()  

        print("=" * 60)  

        log(  
            f"Instagram Zernio publishing failed: {e}"  
        )  

    # =====================================================  
    # YOUTUBE SHORTS  
    # =====================================================  

    try:  

        log(  
            "Uploading YouTube Shorts..."  
        )  

        # =================================================  
        # EXTRACT SEO DATA  
        # =================================================  

        if isinstance(  
            seo,  
            dict  
        ):  

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

            youtube_description = str(  
                seo  
            )  

        # =================================================  
        # THUMBNAIL  
        # =================================================  

        thumbnail_path = (  
            "assets/hook_images/"  
            "promptprohub_hook.jpg"  
        )  

        if os.path.exists(  
            thumbnail_path  
        ):  

            log(  
                f"YouTube thumbnail found: "  
                f"{thumbnail_path}"  
            )  

        else:  

            log(  
                "YouTube thumbnail not found."  
            )  

            thumbnail_path = None  

        # =================================================  
        # YOUTUBE UPLOAD  
        # =================================================  

        upload_to_youtube(  
            video,  
            youtube_title,  
            youtube_description,  
            thumbnail_path  
        )  

        log(  
            "YouTube upload completed."  
        )  

    except Exception as e:  

        print("=" * 60)  
        print(  
            "YOUTUBE UPLOAD FAILED"  
        )  
        print("=" * 60)  

        print(  
            "Error:",  
            e  
        )  

        print(  
            "YouTube traceback:"  
        )  

        traceback.print_exc()  

        print("=" * 60)  

        log(  
            f"YouTube upload failed: {e}"  
        )  

    # =====================================================  
    # COMPLETE  
    # =====================================================  

    log(  
        "Production completed successfully."  
    )  

    print("=" * 60)  
    print(  
        "PROMPTPROHUB AI STUDIO COMPLETED"  
    )  
    print("=" * 60)  

    print(  
        "Video:",  
        video  
    )  

    print(  
        "Status 200:",  
        "TikTok + LinkedIn + TikTok 2 + Pinterest"  
    )  

    print(  
        "Instagram:",  
        "@promptprohub3 via Zernio"  
    )  

    print(  
        "YouTube:",  
        "Shorts"  
    )  

    print("=" * 60)  

except Exception as e:  

    # =====================================================  
    # FULL BOT ERROR  
    # =====================================================  

    print("=" * 60)  
    print("BOT FAILED")  
    print("=" * 60)  

    print(  
        f"ERROR TYPE: {type(e).__name__}"  
    )  

    print(  
        f"ERROR: {repr(e)}"  
    )  

    print("=" * 60)  
    print("FULL TRACEBACK")  
    print("=" * 60)  

    traceback.print_exc()  

    print("=" * 60)  

    log(  
        f"BOT FAILED: "  
        f"{type(e).__name__}: {e}"  
    )  

    raise

============================================================

START BOT

============================================================

if name == "main":

main()
