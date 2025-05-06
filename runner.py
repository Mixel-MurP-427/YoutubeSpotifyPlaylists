#this program is an example use of the API

import config
import read_Spotify_playlist

playlist_page = "https://open.spotify.com/playlist/4rjTXDEitThyBbXnfRJdOV"

read_Spotify_playlist.read_Spotlist(playlist_page, config.config_settings)