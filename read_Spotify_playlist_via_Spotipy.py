import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load credentials from JSON file
with open("API_KEYS/spotipy_creds.json", "r") as f:
    creds = json.load(f)

# Set up Spotify authentication
scope = "playlist-read-private playlist-read-collaborative"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=creds["clientId"],
    client_secret=creds["clientSecret"],
    redirect_uri="http://localhost:8888",
    cache_path="API_KEYS/spotipy_cache.token",
    scope=scope
))

# Function to get all tracks from a playlist
def get_all_playlist_tracks(playlist_id):
    tracks = []
    results = sp.playlist_items(playlist_id, additional_types=['track'])
    tracks.extend(results['items'])

    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    basic_info = []
    for track in tracks:
        if track: # Sometimes track might be None (e.g., deleted)

            song_info = {}
            song_info['title'] = track['track']['name']
            song_info['album'] = track['track']['album']['name']

            artists = []
            for artist_thing in track['track']['artists']:
                artists.append(artist_thing['name'])
            song_info['artist'] = ', '.join(artists)

            basic_info.append(song_info)

    return basic_info


if __name__ == "__main__":

    # Example usage: Replace with your playlist ID (you can find it in the Spotify URL)
    playlist_id = "7qlbZw2xZQvWos9M7uj8Pe"  # e.g., "37i9dQZF1DXcBWIGoYBM5M"

    # Fetch all tracks
    songs = get_all_playlist_tracks(playlist_id)

    for song in songs:
        print(f'{song["title"]} - {song["album"]}: {song["artist"]}')