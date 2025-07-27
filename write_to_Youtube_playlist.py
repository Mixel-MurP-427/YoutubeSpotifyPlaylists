#cred Gemini
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle

# Define scopes for API access
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def create_playlist(youtube, title, privacy_status="private"):
    """Creates a YouTube playlist."""
    request_body = {
        "snippet": {
            "title": title,
            "description": "A playlist created with Python",
        },
        "status": {"privacyStatus": privacy_status},
    }
    request = youtube.playlists().insert(
        part="snippet,status", body=request_body
    )
    response = request.execute()
    return response

def main():
    """Main function to create a playlist."""
    creds = None
    if os.path.exists("API_keys/token.pickle"):
        with open("API_keys/token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    youtube = build("youtube", "v3", credentials=creds)

    playlist_title = "My Awesome Playlist"
    playlist = create_playlist(youtube, playlist_title, "public")
    print(f"Playlist created: {playlist['snippet']['title']} ({playlist['id']})")

print('someting')
main()