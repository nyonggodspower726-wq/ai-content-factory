from google_auth_oauthlib.flow import Flow
import json

CLIENT_SECRET_FILE = "client_secret.json"

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload"
]


flow = Flow.from_client_secrets_file(
    CLIENT_SECRET_FILE,
    scopes=SCOPES,
    redirect_uri="http://localhost:8080"
)


auth_url, state = flow.authorization_url(
    access_type="offline",
    prompt="consent",
    include_granted_scopes="true"
)


print("\nOpen this URL in your browser:\n")
print(auth_url)

print("\nAfter approval, paste the full callback URL here:\n")

callback_url = input("> ")


flow.fetch_token(
    authorization_response=callback_url
)


credentials = flow.credentials


print("\n==============================")
print("NEW YOUTUBE REFRESH TOKEN")
print("==============================\n")

print(credentials.refresh_token)

print("\nCopy this token to Railway:")
print("YOUTUBE_REFRESH_TOKEN")
