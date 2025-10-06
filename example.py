#this program is an example use of the API

import json
from read_Spotify_playlist_via_Spotipy import get_all_playlist_tracks
from Selenium_search import search_songs_with_Selenium
from YoutubeAPI_things import get_authenticated_service, add_song_to_playlist

Spotify_playlist_ID = "4rjTXDEitThyBbXnfRJdOV"
Youtube_playlist_ID = "PLQZJc4l0mTAzUqYSx0297JMVZmXNoXXEG"

"""
print('retrieving songs from Spotify...)
playlist_songs = get_all_playlist_tracks(Spotify_playlist_ID)

print('saving songs...)
with open('playlist.json', 'w') as myFile:
    json.dump(playlist_songs, myFile)
"""

#this is a hack
playlist_songs = {
    "1": {
        "title": "The Rebel Path",
        "artist": "P.T. Adamczyk",
        "album": "Cyberpunk 2077 - Original Score"
    },
    "2": {
        "title": "Betelgeuse Boogaloo",
        "artist": "Theatre Of Delays",
        "album": "Betelgeuse Boogaloo"
    },
    "3": {
        "title": "Use of Force",
        "artist": "Le Castle Vania",
        "album": "Payday"
    },
    "4": {
        "title": "End of Line",
        "artist": "Daft Punk",
        "album": "TRON: Legacy - The Complete Edition (Original Motion Picture Soundtrack)"
    },
    "5": {
        "title": "6.24",
        "artist": "Danger",
        "album": "Furi (Original Game Soundtrack)"
    },
    "6": {
        "title": "The Orb",
        "artist": "Daniel Deluxe",
        "album": "Ghostrunner (Original Soundtrack)"
    },
    "7": {
        "title": "Undefined",
        "artist": "Bad Computer",
        "album": "Undefined"
    },
    "8": {
        "title": "4Me",
        "artist": "Bad Computer",
        "album": "4Me"
    },
    "9": {
        "title": "Hypnocurrency",
        "artist": "Rezz",
        "album": "Hypnocurrency"
    },
    "10": {
        "title": "Infraliminal",
        "artist": "REZZMAU5",
        "album": "Infraliminal"
    },
    "11": {
        "title": "1:30",
        "artist": "Danger",
        "album": "July 2013"
    },
    "12": {
        "title": "Spoiler - Original Mix",
        "artist": "Hyper",
        "album": "Lies"
    },
    "13": {
        "title": "Merge",
        "artist": "Theatre Of Delays",
        "album": "This Is Not an Album, Pt. 2"
    },
    "14": {
        "title": "Timefracture",
        "artist": "Bad History",
        "album": "Timefracture"
    },
    "15": {
        "title": "22:39",
        "artist": "Danger",
        "album": "Origins"
    },
    "16": {
        "title": "Terrabot",
        "artist": "Waveshaper",
        "album": "Terrabot"
    },
    "17": {
        "title": "Stealth Mech",
        "artist": "Front Line Assembly",
        "album": "AirMech"
    },
    "18": {
        "title": "CALAMITOUS",
        "artist": "VALORANT",
        "album": "MV//MNT VOL. 02"
    },
    "19": {
        "title": "Full Moon 2.0",
        "artist": "RJ Pasin",
        "album": "Full Moon"
    },
    "20": {
        "title": "The Cyber Grind",
        "artist": "meganeko",
        "album": "The Cyber Grind"
    },
    "21": {
        "title": "HEIST",
        "artist": "VALORANT",
        "album": "MV//MNT VOL. 02"
    },
    "22": {
        "title": "Slinky",
        "artist": "Navie D",
        "album": "Music to Banana To"
    },
    "23": {
        "title": "OPEN UR EYE",
        "artist": "Rezz",
        "album": "CAN YOU SEE ME?"
    },
    "24": {
        "title": "Komputer Problems (The Otherside Series, Vol. 3)",
        "artist": "Le Castle Vania",
        "album": "Komputer Problems (The Otherside Series, Vol. 3)"
    },
    "25": {
        "title": "Extreme Drift",
        "artist": "Absolute Valentine",
        "album": "Police Heartbreaker"
    },
    "26": {
        "title": "\u041c\u0443\u0441\u043e\u0440\u0449\u0438\u043a\u0438",
        "artist": "P.T. Adamczyk",
        "album": "Cyberpunk 2077 - Original Score"
    },
    "27": {
        "title": "The Upside-Down (Stranger Things Inspired)",
        "artist": "INTERCOM",
        "album": "The Upside-Down (Stranger Things Inspired)"
    },
    "28": {
        "title": "Murder",
        "artist": "Soulji",
        "album": "Black Mask"
    },
    "29": {
        "title": "Gravastars",
        "artist": "Epic Mountain",
        "album": "Kurzgesagt, Vol. 11 (Original Motion Picture Soundtrack)"
    },
    "30": {
        "title": "Hex",
        "artist": "Simon Chylinski",
        "album": "Hex"
    }
}
"""
search_queries = []
for i in range(1, len(playlist_songs)+1):
    search_queries.append(f"{playlist_songs[str(i)]['title']} {playlist_songs[str(i)]['artist']} {playlist_songs[str(i)]['album']}")

Youtube_song_IDs = search_songs_with_Selenium(search_queries)

with open('song_IDs.json', 'w') as myFile:
    json.dump(Youtube_song_IDs, myFile)
"""
with open('playlist.json', 'r') as myFile:
    Youtube_song_IDs = json.load(myFile)

#setup Youtube client
youtube = get_authenticated_service()


for ID in Youtube_song_IDs:
    add_song_to_playlist(youtube, Youtube_playlist_ID, ID)