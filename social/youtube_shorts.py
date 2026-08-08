import os
import json

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

from config import (
    YOUTUBE_CLIENT_ID,
    YOUTUBE_CLIENT_SECRET,
    YOUTUBE_REFRESH_TOKEN,
)


SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload"
]


# ============================================================
# SEO DATA NORMALIZER
# ============================================================

def normalize_seo(title, description):

    """
    Accepts normal strings, dictionaries, or JSON strings.

    This allows bot.py to safely pass the SEO object directly.
    """

    seo_data = None

    # ----------------------------------------
    # TITLE MAY ACTUALLY BE SEO DATA
    # ----------------------------------------

    if isinstance(title, dict):

        seo_data = title

    elif isinstance(title, str):

        cleaned = title.strip()

        if cleaned.startswith("{"):

            try:

                parsed = json.loads(cleaned)

                if isinstance(parsed, dict):

                    seo_data = parsed

            except Exception:

                seo_data = None


    # ----------------------------------------
    # EXTRACT SEO TITLE
    # ----------------------------------------

    if seo_data:

        selected_title = (

            seo_data.get("click_title")

            or seo_data.get("title")

            or seo_data.get("seo_title")

            or "AI Tools That Save You Hours of Work"

        )

        # Prefer generated description
        selected_description = (

            seo_data.get("description")

            or description

            or "Discover powerful AI tools and productivity systems."

        )

        # Add hashtags when available
        hashtags = seo_data.get(
            "hashtags",
            []
        )

        if isinstance(hashtags, list) and hashtags:

            hashtag_text = " ".join(
                str(tag)
                for tag in hashtags
            )

            if hashtag_text not in str(
                selected_description
            ):

                selected_description = (
                    str(selected_description)
                    + "\n\n"
                    + hashtag_text
                )

        return (
            str(selected_title),
            str(selected_description)
        )


    # ----------------------------------------
    # NORMAL STRING TITLE
    # ----------------------------------------

    selected_title = str(
        title
        if title
        else "AI Tools That Save You Hours of Work"
    )


    selected_description = str(

        description

        if description

        else "Discover powerful AI tools and productivity systems."

    )


    return (
        selected_title,
        selected_description
    )


# ============================================================
# YOUTUBE SHORTS UPLOADER
# ============================================================

def upload_to_youtube(
    video_path,
    title,
    description,
    thumbnail_path=None
):

    print("=" * 60)
    print("PROMPTPROHUB YOUTUBE SHORTS UPLOADER")
    print("=" * 60)


    # ========================================================
    # DEBUG
    # ========================================================

    print(
        "CLIENT ID:",
        YOUTUBE_CLIENT_ID
    )

    print(
        "CLIENT SECRET EXISTS:",
        bool(YOUTUBE_CLIENT_SECRET)
    )

    print(
        "REFRESH TOKEN EXISTS:",
        bool(YOUTUBE_REFRESH_TOKEN)
    )

    print(
        "VIDEO:",
        video_path
    )

    print(
        "THUMBNAIL:",
        thumbnail_path
    )

    print(
        "RAW TITLE:",
        repr(title)
    )

    print(
        "RAW DESCRIPTION:",
        repr(description)
    )

    print("=" * 60)


    # ========================================================
    # NORMALIZE SEO
    # ========================================================

    title, description = normalize_seo(
        title,
        description
    )


    print(
        "FINAL YOUTUBE TITLE:",
        title
    )

    print(
        "FINAL DESCRIPTION:",
        description
    )


    # ========================================================
    # FALLBACK TITLE
    # ========================================================

    if not title.strip():

        title = (
            "AI Tools That Save You "
            "Hours of Work"
        )


    # ========================================================
    # FALLBACK DESCRIPTION
    # ========================================================

    if not description.strip():

        description = (
            "Discover powerful AI tools, "
            "prompts and productivity systems "
            "from PromptProHub."
        )


    # ========================================================
    # CHECK VIDEO
    # ========================================================

    if not video_path:

        print(
            "No video path supplied."
        )

        return False


    if not os.path.exists(video_path):

        print(
            "Video not found:",
            video_path
        )

        return False


    # ========================================================
    # THUMBNAIL NOTICE
    # ========================================================

    if thumbnail_path:

        if os.path.exists(thumbnail_path):

            print("=" * 60)
            print(
                "THUMBNAIL DETECTED"
            )
            print(
                "This uploader is configured for YouTube Shorts."
            )
            print(
                "The custom-thumbnail API call is intentionally skipped."
            )
            print(
                "The thumbnail will NOT be uploaded through the API."
            )
            print("=" * 60)

        else:

            print(
                "Thumbnail file not found:",
                thumbnail_path
            )


    try:

        # ====================================================
        # GOOGLE CREDENTIALS
        # ====================================================

        credentials = Credentials(

            token=None,

            refresh_token=(
                YOUTUBE_REFRESH_TOKEN
            ),

            token_uri=(
                "https://oauth2.googleapis.com/token"
            ),

            client_id=(
                YOUTUBE_CLIENT_ID
            ),

            client_secret=(
                YOUTUBE_CLIENT_SECRET
            ),

            scopes=SCOPES

        )


        # ====================================================
        # YOUTUBE CLIENT
        # ====================================================

        youtube = build(

            "youtube",

            "v3",

            credentials=credentials

        )


        # ====================================================
        # VIDEO METADATA
        # ====================================================

        body = {

            "snippet": {

                "title": str(title)[:100],

                "description": str(
                    description
                ),

                "categoryId": "22"

            },

            "status": {

                "privacyStatus": "public",

                "selfDeclaredMadeForKids": False

            }

        }


        # ====================================================
        # VIDEO FILE
        # ====================================================

        media = MediaFileUpload(

            video_path,

            mimetype="video/mp4",

            chunksize=-1,

            resumable=True

        )


        # ====================================================
        # UPLOAD
        # ====================================================

        print("=" * 60)
        print("UPLOADING YOUTUBE SHORT...")
        print("=" * 60)


        request = youtube.videos().insert(

            part="snippet,status",

            body=body,

            media_body=media

        )


        response = None
