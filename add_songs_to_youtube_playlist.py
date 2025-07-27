#cred to Copilot
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

def get_authenticated_service(api_key, client_secret):
    # Use API key for simple requests, but for modifying playlists, OAuth is required.
    scopes = ["https://www.googleapis.com/auth/youtube"]
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secret, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)
    return youtube

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

def main():
    #get keys
    api_key_path = "API_keys/key.txt"
    with open(api_key_path, "r") as f:
        api_key = f.readline().strip() #api_key is not accessed in this program
        OAuth_client_secret_path = f.readline().strip()
        print((api_key, OAuth_client_secret_path))
    #setup Youtube client
    youtube = get_authenticated_service(api_key, OAuth_client_secret_path)

    playlist_id = "PLQZJc4l0mTAzUqYSx0297JMVZmXNoXXEG"
    songs = [
        "Wake Up Alan Walker Neon Nights",
        "VGR Smash Bros Melee",
        "Crab Rave Noisestorm"
    ]
    for song in songs:
        video_id = search_song(youtube, song)
        if video_id:
            add_song_to_playlist(youtube, playlist_id, video_id)
            print(f"Added '{song}' to playlist.")
        else:
            print(f"Song '{song}' not found.")

if __name__ == "__main__":
    print('going!')
    main()