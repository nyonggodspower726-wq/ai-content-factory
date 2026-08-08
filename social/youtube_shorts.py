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

    print("===== YOUTUBE DEBUG =====")

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
        "TITLE:",
        repr(title)
    )

    print(
        "DESCRIPTION:",
        repr(description)
    )

    print("=========================")


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

    if not os.path.exists(video_path):

        print(
            "Video not found:",
            video_path
        )

        return False


    # =====================================
    # CHECK THUMBNAIL
    # =====================================

    if thumbnail_path:

        if not os.path.exists(
            thumbnail_path
        ):

            print(
                "Thumbnail not found:",
                thumbnail_path
            )

            thumbnail_path = None


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

                print(
                    "Uploading...",
                    int(
                        status.progress() * 100
                    ),
                    "%"
                )


        # =================================
        # VIDEO UPLOADED
        # =================================

        video_id = response["id"]


        print("=" * 60)

        print(
            "YouTube Upload Successful!"
        )

        print(
            "Video ID:",
            video_id
        )

        print(
            "Video URL:",
            f"https://youtu.be/{video_id}"
        )

        print("=" * 60)


        # =================================
        # CUSTOM THUMBNAIL
        # =================================

        if thumbnail_path:

            try:

                print("=" * 60)

                print(
                    "SETTING YOUTUBE THUMBNAIL..."
                )

                print(
                    "Thumbnail:",
                    thumbnail_path
                )

                print("=" * 60)


                thumbnail_media = (
                    MediaFileUpload(

                        thumbnail_path,

                        mimetype="image/jpeg",

                        resumable=False

                    )
                )


                thumbnail_request = (
                    youtube.thumbnails().set(

                        videoId=video_id,

                        media_body=(
                            thumbnail_media
                        )

                    )
                )


                thumbnail_response = (
                    thumbnail_request.execute()
                )


                print("=" * 60)

                print(
                    "YOUTUBE THUMBNAIL SET SUCCESSFULLY"
                )

                print("=" * 60)


            except Exception as e:

                print("=" * 60)

                print(
                    "THUMBNAIL FAILED"
                )

                print(
                    type(e).__name__
                )

                print(
                    str(e)
                )

                print("=" * 60)


        else:

            print(
                "No custom thumbnail supplied."
            )


        return video_id


    except Exception as e:

        print("=" * 60)

        print(
            "YOUTUBE ERROR"
        )

        print(
            type(e).__name__
        )

        print(
            str(e)
        )

        print("=" * 60)

        return False
