#this program contains all fuctions pertaining to the Youtube API

import os

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from googleapiclient.errors import HttpError


#initialize Youtube object
def get_authenticated_service(): #credit: "https://stackoverflow.com/a/77714081"
    creds = None
    scopes = ['https://www.googleapis.com/auth/youtube']
    token_path = 'API_keys/token.json'

    #get keys
    api_key_path = "API_keys/key.txt"
    with open(api_key_path, "r") as f:
        api_key = f.readline().strip() #api_key is unaccessed in this program
        OAuth_client_secret_path = f.readline().strip()

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, scopes)

    # If there are no (valid) user credentials available, prompt the user to log in.
    if not creds or not creds.valid:
        # try to refresh; if refresh fails, remove token and re-run the flow
        try:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
        except RefreshError:
            try:
                os.remove(token_path)
            except OSError:
                pass
            creds = None

        if not creds:
            flow = InstalledAppFlow.from_client_secrets_file(
                OAuth_client_secret_path, scopes)
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_path, 'w') as token:
                token.write(creds.to_json())

    try:
        return build('youtube', 'v3', credentials=creds)
    except HttpError as error:
        # TODO(developer) - any errors returned.
        print(f'An error occurred: {error}')


def search_song_with_YoutubeAPI(youtube, query):
    request = youtube.search().list(
        q=query,
        part="id,snippet",
        maxResults=1,
        type="video",
        videoCategoryId="10" # Music category
    )
    response = request.execute()
    items = response.get("items", [])
    print(f"items == {items}")
    if items:
        return items[0]["id"]["videoId"]
    return None


def add_song_to_playlist(youtube, playlist_id, video_id):
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }
    )
    response = request.execute()
    return response