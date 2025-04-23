import json
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

print('program running!')

driver = webdriver.Chrome()
driver.get("https://open.spotify.com/playlist/4rjTXDEitThyBbXnfRJdOV") #put the Spotify playlist url here
assert "Spotify" in driver.title and "playlist" in driver.title

print('driver opened!')


playlist = {}

#constants
#songs_path = "/html/body/div[5]/div/div[2]/div[5]/div/div[2]/div[2]/div/main/section/div[2]/div[3]/div/div[1]/div/div[2]/div[2]" #parent element of all songs
song_path = '//div[@data-testid="tracklist-row"]'
index_path = './div/div/span'
title_path = './div/div/a/div'
artist_path = './div/div/span/div/a'
album_path = './div/span/a'

time.sleep(1)
print('going')
for _ in range(40):
    time.sleep(0.25)
    song_elements = driver.find_elements(By.XPATH, song_path)
    print(len(song_elements))
    for song_element in song_elements:
        song_info = {'title': song_element.find_element(By.XPATH, title_path).text,
            'artist': song_element.find_element(By.XPATH, artist_path).text,
            'album': song_element.find_element(By.XPATH, album_path).text
          }
            
        index = song_element.find_element(By.XPATH, index_path).text

        #print(f"Index: {index}, Title: {title}, Artist: {artist}, Album: {album}")
        playlist[index] = song_info
        print(index, song_info)




"""
for songElem in []:

    elem = driver.find_element(By.XPATH, "/html/body/div[5]/div/div[2]/div[5]/div/div[2]/div[2]/div/main/section/div[2]/div[3]/div/div[1]/div/div[2]/div[2]/div[1]")
    elem.click()
    assert "No results found." not in driver.page_source
    time.sleep(2)
"""



driver.close()
print('closed successfully!')
"""
#save data
with open('playlist.json', 'w') as myFile:
    json.dump(playlist, myFile)"""