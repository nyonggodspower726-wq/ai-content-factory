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


def upload_to_youtube(video_path, title, description):

    print("===== YOUTUBE DEBUG =====")
    print("CLIENT ID:", YOUTUBE_CLIENT_ID)
    print("CLIENT SECRET EXISTS:", bool(YOUTUBE_CLIENT_SECRET))
    print("REFRESH TOKEN EXISTS:", bool(YOUTUBE_REFRESH_TOKEN))
    print("ORIGINAL TITLE:", repr(title))
    print("ORIGINAL DESCRIPTION:", repr(description))
    print("=========================")

    # Fix empty title problem
    if not title or not str(title).strip():
        title = "AI Tools That Save You Time Every Day"

    if not description or not str(description).strip():
        description = "Discover powerful AI tools and productivity tips."

    if not os.path.exists(video_path):
        print("Video not found:", video_path)
        return False

    try:

        credentials = Credentials(
            token=None,
            refresh_token=YOUTUBE_REFRESH_TOKEN,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=YOUTUBE_CLIENT_ID,
            client_secret=YOUTUBE_CLIENT_SECRET,
            scopes=SCOPES,
        )


        youtube = build(
            "youtube",
            "v3",
            credentials=credentials,
        )


        body = {
            "snippet": {
                "title": title[:100],
                "description": description,
                "categoryId": "22",
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False,
            },
        }


        media = MediaFileUpload(
            video_path,
            mimetype="video/mp4",
            chunksize=-1,
            resumable=True,
        )


        request = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media,
        )


        response = None


        while response is None:

            status, response = request.next_chunk()

            if status:
                print(
                    f"Uploading... {int(status.progress()*100)}%"
                )


        print("==============================")
        print("YouTube Upload Successful!")
        print(
            "Video URL:",
            f"https://youtu.be/{response['id']}"
        )
        print("==============================")


        return response["id"]


    except Exception as e:

        print("==============================")
        print("YOUTUBE ERROR")
        print(type(e).__name__)
        print(str(e))
        print("==============================")

        return False
