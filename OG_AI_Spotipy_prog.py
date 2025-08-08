import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load credentials from JSON file
with open("spotipy_creds.json", "r") as f:
    creds = json.load(f)

# Set up Spotify authentication
scope = "playlist-read-private playlist-read-collaborative"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=creds["client_id"],
    client_secret=creds["client_secret"],
    redirect_uri=creds["redirect_uri"],
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

    return tracks

# Example usage: Replace with your playlist ID (you can find it in the Spotify URL)
playlist_id = "YOUR_PLAYLIST_ID_HERE"  # e.g., "37i9dQZF1DXcBWIGoYBM5M"

# Fetch all tracks
songs = get_all_playlist_tracks(playlist_id)

# Print song details
for idx, item in enumerate(songs, start=1):
    track = item['track']
    if track:  # Sometimes track might be None (e.g., deleted)
        name = track['name']
        artists = ", ".join([artist['name'] for artist in track['artists']])
        print(f"{idx}. {name} – {artists}")
