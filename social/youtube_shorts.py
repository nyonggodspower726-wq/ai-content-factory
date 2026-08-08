import os

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


def upload_to_youtube(
    video_path,
    title,
    description,
    thumbnail_path=None
):

    print("=" * 60)
    print("YOUTUBE UPLOAD ENGINE")
    print("=" * 60)

    print("VIDEO:", video_path)
    print("TITLE:", repr(title))
    print("DESCRIPTION:", repr(description))

    # =====================================
    # THUMBNAIL NOTICE
    # =====================================

    if thumbnail_path:

        print(
            "Custom thumbnail generated locally:",
            thumbnail_path
        )

        print(
            "Custom thumbnail upload disabled."
        )

        print(
            "YouTube will use its automatic thumbnail."
        )

    # =====================================
    # FALLBACK METADATA
    # =====================================

    if not title or not str(title).strip():

        title = (
            "AI Tools That Save You "
            "Hours of Work"
        )

    if not description or not str(
        description
    ).strip():

        description = (
            "Discover powerful AI tools "
            "and productivity systems."
        )

    # =====================================
    # CHECK VIDEO
    # =====================================

    if not video_path:

        print("Video path is empty.")
        return False

    if not os.path.exists(video_path):

        print(
            "Video not found:",
            video_path
        )

        return False

    try:

        # =================================
        # GOOGLE CREDENTIALS
        # =================================

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

        # =================================
        # YOUTUBE CLIENT
        # =================================

        youtube = build(

            "youtube",
            "v3",
            credentials=credentials

        )

        # =================================
        # VIDEO METADATA
        # =================================

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

        # =================================
        # VIDEO FILE
        # =================================

        media = MediaFileUpload(

            video_path,

            mimetype="video/mp4",

            chunksize=-1,

            resumable=True

        )

        # =================================
        # UPLOAD VIDEO
        # =================================

        print("=" * 60)
        print("UPLOADING YOUTUBE VIDEO")
        print("=" * 60)

        request = youtube.videos().insert(

            part="snippet,status",

            body=body,

            media_body=media

        )

        response = None

        while response is None:

            status, response = (
                request.next_chunk()
            )

            if status:

                progress = int(
                    status.progress() * 100
                )

                print(
                    f"Uploading... {progress}%"
                )

        # =================================
        # SUCCESS
        # =================================

        video_id = response["id"]

        print("=" * 60)
        print("YOUTUBE UPLOAD SUCCESSFUL")
        print("=" * 60)

        print(
            "Video ID:",
            video_id
        )

        print(
            "Video URL:",
            f"https://youtu.be/{video_id}"
        )

        print("=" * 60)

        print(
            "Custom thumbnail upload skipped."
        )

        print(
            "No thumbnail permission error."
        )

        print("=" * 60)

        return video_id

    except Exception as e:

        print("=" * 60)
        print("YOUTUBE UPLOAD FAILED")
        print("=" * 60)

        print(
            type(e).__name__
        )

        print(
            str(e)
        )

        print("=" * 60)

        return False
