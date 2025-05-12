import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time

#constants
song_path = '//div[@data-testid="tracklist-row"]'
index_path = './div/div/span'
title_path = './div/div/a/div'
artist_path = './div/div/span/div/a'
album_path = './div/span/a'

def read_Spotlist(rsURL, rsConfig):
    rsErrorCount = 0

    driver = webdriver.Chrome()
    driver.get(rsURL) #put the Spotify playlist url here
    assert "Spotify" in driver.title and "playlist" in driver.title

    playlist = {}

    time.sleep(rsConfig["initial wait time"])

    for _ in range(rsConfig["scan iterations"]):
        time.sleep(rsConfig["iteration pause time"])

        song_elements = driver.find_elements(By.XPATH, song_path)

        for song_element in song_elements:
            try:
                song_info = {'title': song_element.find_element(By.XPATH, title_path).text,
                    'artist': song_element.find_element(By.XPATH, artist_path).text,
                    'album': song_element.find_element(By.XPATH, album_path).text
                } 
                index = int(song_element.find_element(By.XPATH, index_path).text)

            except (NoSuchElementException, StaleElementReferenceException, ValueError):
                rsErrorCount += 1 #this line of code is basically worthless
            else:
                playlist[index] = song_info

        if rsConfig["auto-save each iteration"]:
            with open('playlist.json', 'w') as myFile:
                json.dump(playlist, myFile)


    driver.close()
    #print('closed successfully!')
    print(f"Done!\nNumber of songs found: {len(playlist)}\nNumber of uncaught elements: {rsErrorCount}")
    if not rsConfig["auto-save each iteration"]:
        return playlist