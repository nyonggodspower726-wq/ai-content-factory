def upload_to_youtube(video_path, title, description):

    print("===== YOUTUBE DEBUG =====")
    print("CLIENT ID:", YOUTUBE_CLIENT_ID)
    print("CLIENT SECRET EXISTS:", bool(YOUTUBE_CLIENT_SECRET))
    print("REFRESH TOKEN EXISTS:", bool(YOUTUBE_REFRESH_TOKEN))
    print("=========================")

    if not os.path.exists(video_path):
        print("Video not found.")
        return False

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
            "title": title,
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
            print(f"Uploading... {int(status.progress() * 100)}%")

    print("YouTube Upload Successful!")
    print(f"https://youtu.be/{response['id']}")

    return response["id"]
