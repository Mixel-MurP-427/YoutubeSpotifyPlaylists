#This program contains every step needed to create a Youtube replica of your Spotify playlist
#note config variables below
#see README for more info

import json
from read_Spotify_playlist_via_Spotipy import get_all_playlist_tracks
from Selenium_search import search_songs_with_Selenium
from YoutubeAPI_things import get_authenticated_service, add_song_to_playlist

# THE USER WILL WANT TO CONFIGURE THESE VARIALBES
Spotify_playlist_ID = '4rjTXDEitThyBbXnfRJdOV' # from https://open.spotify.com/playlist/4rjTXDEitThyBbXnfRJdOV, the Spotify playlist I am reading from
Youtube_playlist_ID = 'PLQZJc4l0mTAzUqYSx0297JMVZmXNoXXEG' # from https://music.youtube.com/playlist?list=PLQZJc4l0mTAzUqYSx0297JMVZmXNoXXEG, the Youtube playlist I am writing to
songs_save_path = 'playlist.json'
IDs_save_path = 'song_IDs.json'


#ask user which steps to complete
answer = 'h'
while answer == 'h': #this could also be set to while True, but who cares?
    answer = input('Which steps would you like to complete? (type "h" for help): ')
    if answer != 'h': break
    print(
        '''    Step 1 retrieves the songs titles and basic data from your Spotify playlist.
    Step 2 searches Youtube for these songs.
    Step 3 adds these songs to your Youtube playlist.
    To run only one step, type it's number, e.g. "1" for step 1.
    To run multiple steps, type the number of each step, e.g. "23" to run steps 2 and 3.
    To run the whole program, type "123"\n''')



#Step 1
if  '1' in answer:
    print('Step 1\nretrieving songs from Spotify...')
    playlist_songs = get_all_playlist_tracks(Spotify_playlist_ID)

    #save the song data
    print('songs retrieved\nsaving songs...')
    with open(songs_save_path, 'w') as myFile:
        json.dump(playlist_songs, myFile)
    print(f'songs saved to "{songs_save_path}"')


#Step 2
if '2' in answer:
    print('Step 2')

    #get playlist_songs from songs_save_path if Step 1 was not run
    if not '1' in answer:
        with open(songs_save_path, 'r') as myFile:
            playlist_songs = json.load(myFile)

    #generate search queries from data
    print('searching Youtube for song IDs...')
    search_queries = []
    for i in range(len(playlist_songs)):
        search_queries.append(f"{playlist_songs[i]['title']} {playlist_songs[i]['artist']} {playlist_songs[i]['album']}")

    Youtube_song_IDs = search_songs_with_Selenium(search_queries)

    #save the song IDs
    print('song IDs retrieved\nsaving IDs...')
    with open(IDs_save_path, 'w') as myFile:
        json.dump(Youtube_song_IDs, myFile)
    print(f'IDs saved to "{IDs_save_path}"')


#Step 3
if '3' in answer:
    print('Step 3')

    #get Youtube_song_IDs from IDs_save_path if Step 2 was not run
    if not '2' in answer:
        with open(IDs_save_path, 'r') as myFile:
            Youtube_song_IDs = json.load(myFile)

    print("Let's see if we can login to the Youtube API...")
    youtube = get_authenticated_service() #setup Youtube client

    print("Alrighty, we are logged in!\nadding songs to Youtube playlist...")
    for ID in Youtube_song_IDs:
        add_song_to_playlist(youtube, Youtube_playlist_ID, ID)
    print('songs added')


print('end of program!')