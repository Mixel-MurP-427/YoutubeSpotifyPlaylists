# Put your Spotify playlists on Youtube!

## Getting Started
Clone this repo and install the dependencies:

    pip install -r requirements.txt

## Usage
[main.py](main.py) is basically all you will ever need to interact with. Simply edit the playlist ID variables on lines 11 and 12 and run the program. It will ask you which "steps" you want to complete. For my TLDRers, just type "123" and enter. It will run the whole program.

### For those who are curious about the processes inside [main.py](main.py):
The program is broken up into three sections or "steps":
1. **<ins>Read the songs from the Spotify playlist via Spotipy.</ins>** Using `read_Spotify_playlist_via_Spotipy.get_all_playlist_tracks`, Spotipy logs into Spotify and then asks for a boatload of data about each song. The function narrows this data down to a list of dictionaries for each song with title, album, and artist data and then returns the list.
2. **<ins>Search for these songs on Youtube Music via Selenium.</ins>** The program uses `Selenium_search.search_songs_with_Selenium` to open [Youtube Music](https://music.youtube.com/) in the browser and searches for each song via the data collected previously. It clicks some buttons to find the first song (not video!), then grabs the share link and extracts the video ID. The function returns a list of the IDs.
3. **<ins>Add the songs to the Youtube playlist.</ins>** `YoutubeAPI_things.get_authenticated_service` logs into Google and gets the authentication needed to use the Youtube API. `YoutubeAPI_things.add_song_to_playlist` simply uses the Youtube API and the previously created list of video IDs to add each song to the Youtube playlist.

And that's it!

## Links to documentation for APIs used
### Spotipy
https://spotipy.readthedocs.io/en/2.25.1/#
### Google and Youtube
https://developers.google.com/youtube/v3/docs  
https://github.com/youtube/api-samples/blob/master/python/README.md
### Selenium
https://selenium-python.readthedocs.io/
