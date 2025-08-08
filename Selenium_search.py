#this function is an alternative to using the Youtube API to search for music.
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time

#constants
#searchbar = '//*[@id="input"]'
song_filter_button = '//yt-formatted-string[text() = "Songs"]'
'//*[@id="button-shape"]/button/yt-touch-feedback-shape/div/div[2]' #menu button?
'//*[@id="contents"]/ytmusic-responsive-list-item-renderer[1]' #first song item
'//*ytmusic-responsive-list-item-renderer[1]/ytmusic-menu-renderer/[1][@id="button-shape"]/button' # first song menu button
'//*[@id="navigation-endpoint"]'

def search_song_with_Selenium(youtube, query):
    print('something')

    search_phrase = query.replace(' ', '+')

    driver = webdriver.Chrome()
    driver.get(f"https://music.youtube.com/search?q={search_phrase}") #put the Spotify playlist url here
    assert "Youtube Music" in driver.title

    song_filter_element = driver.find_element(By.XPATH, song_filter_button)
    song_filter_element.click()

    time.sleep(5)

    driver.close()
