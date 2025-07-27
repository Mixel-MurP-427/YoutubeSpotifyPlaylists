import os

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError



def build_service(credentials): #credit: "https://stackoverflow.com/a/77714081"
    creds = None
    scope = 'https://www.googleapis.com/auth/youtube'

    #get keys
    api_key_path = "API_keys/key.txt"
    with open(api_key_path, "r") as f:
        api_key = f.readline().strip() #api_key is unaccessed in this program
        OAuth_client_secret_path = f.readline().strip()
        print((api_key, OAuth_client_secret_path))

    if os.path.exists(OAuth_client_secret_path):
        creds = Credentials.from_authorized_user_file(OAuth_client_secret_path, scope)

    # If there are no (valid) user credentials available, prompt the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials, scope)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(user_token, 'w') as token:
            token.write(creds.to_json())
    try:
        return build('youtube', 'v3', credentials=creds)
    except HttpError as error:
        # TODO(developer) - any errors returned.
        print(f'An error occurred: {error}')






def search_song(youtube, query):
    request = youtube.search().list(
        q=query,
        part="id,snippet",
        maxResults=1,
        type="video",
        videoCategoryId="10"  # Music category
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

def main(songs):
    
    #setup Youtube client
    youtube = get_authenticated_service(api_key, OAuth_client_secret_path)

    playlist_id = "PLQZJc4l0mTAzUqYSx0297JMVZmXNoXXEG"

    for song in songs:
        video_id = search_song(youtube, song)
        if video_id:
            add_song_to_playlist(youtube, playlist_id, video_id)
            print(f"Added '{song}' to playlist.")
        else:
            print(f"Song '{song}' not found.")

if __name__ == "__main__":
    print('going!')
    main([
        "Wake Up Alan Walker Neon Nights",
        "VGR Smash Bros Melee",
        "Crab Rave Noisestorm"
    ])