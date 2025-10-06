#TODO desc

import json

import config
from read_Spotify_playlist_via_Selenium import read_Spotlist
#TODO import YoutubeAPI_things

Spotify_playlist_page = "https://open.spotify.com/playlist/7qlbZw2xZQvWos9M7uj8Pe"
Youtube_playlist_ID = "PLQZJc4l0mTAzUqYSx0297JMVZmXNoXXEG"

playlist_songs = read_Spotlist(Spotify_playlist_page, config.config_settings)

with open('playlist.json', 'w') as myFile:
    json.dump(playlist_songs, myFile)
"""
#setup Youtube client
youtube = get_authenticated_service()


for song in playlist_songs:
    video_id = search_song(youtube, song)
    if video_id:
        add_song_to_playlist(youtube, Youtube_playlist_ID, video_id)
        print(f"Added '{song}' to playlist.")
    else:
        print(f"Song '{song}' not found.")"""