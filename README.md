# Put your Spotify playlists on Youtube!
(Using just Python!)

## Setup
### Installation
Clone this repo and install the dependencies:

    pip install -r requirements.txt

The code in this repository *should* work with the latest version of the required libraries, but just in case, here are the versions in place at the publication of the repository:

    google-api-python-client  2.169.0
    google-auth-oauthlib      1.2.2
    selenium                  4.27.1
    spotipy                   2.25.1

### Getting your API keys

- To edit Youtube playlists, you will need to make a Google Dev project, enable "YouTube Data API v3", create OAuth Client ID credentials (select the "desktop/installed app" type), and save the client secret file inside the "./API_keys" directory of this repository.

- Create an "./API_keys/key.txt" file and write the filepath to your client secret file on the second line. Optional: Put your YouTube Data API v3 key on the first line. (It won't really do anything, but why not save it?)

- [Setup your Spotify oauth](https://github.com/spotipy-dev/spotipy/blob/2.22.1/TUTORIAL.md) and save the client secret as "./API_keys/spotipy_creds.json". It's contents should look like this:

        {"clientId": "abc123efg456abc123efg456abc123efg456", "clientSecret": "abc123efg456abc123efg456abc123efg456"}

## Usage
[main.py](main.py) is basically all you will ever need to interact with. Simply edit the playlist ID variables on lines 11 and 12 and run the program. It will ask you which "steps" you want to complete. For my TLDRers, just type "123" and enter. It will run the whole program.

### For those who are curious about the processes inside [main.py](main.py):
The program is broken up into three sections or "steps":
1. **Read the songs from the Spotify playlist via Spotipy.** Using [get_all_playlist_tracks()](https://github.com/Mixel-MurP-427/YoutubeSpotifyPlaylists/blob/main/read_Spotify_playlist_via_Spotipy.py#L22), Spotipy logs into Spotify and then asks for a boatload of data about each song. The function narrows this data down to a list of dictionaries for each song with title, album, and artist data and then returns the list.
2. **Search for these songs on Youtube Music via Selenium.** The program uses [search_songs_with_Selenium()](https://github.com/Mixel-MurP-427/YoutubeSpotifyPlaylists/blob/main/Selenium_search.py#L28) to open [Youtube Music](https://music.youtube.com/) in the browser and searches for each song via the data collected previously. It clicks some buttons to find the first song (not video!), then grabs the share link and extracts the video ID. The function returns a list of the IDs.
3. **Add the songs to the Youtube playlist.** The [get_authenticated_service()](https://github.com/Mixel-MurP-427/YoutubeSpotifyPlaylists/blob/main/YoutubeAPI_things.py#L13) function logs into Google and gets the authentication needed to use the Youtube API. [add_song_to_playlist()](https://github.com/Mixel-MurP-427/YoutubeSpotifyPlaylists/blob/main/YoutubeAPI_things.py#L62) simply uses the Youtube API and the previously created list of video IDs to add each song to the Youtube playlist.

And that's it!

## Links to documentation for APIs used
### Spotipy
https://spotipy.readthedocs.io/en/2.25.1/#
### Google and Youtube
https://developers.google.com/youtube/v3/docs  
https://developers.google.com/identity/protocols/oauth2  
https://github.com/youtube/api-samples/blob/master/python/README.md
### Selenium
https://selenium-python.readthedocs.io/
