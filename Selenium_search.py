#This function is an alternative to using the Youtube API to search for music.
#It uses Selenium to open https://music.youtube.com/ and manually search for songs

import re
import math
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException


#constants
xml_paths = {
#   'searchbar': '//*[@id="input"]',
    'song_filter_button': '//yt-formatted-string[text() = "Songs"]',
    'X_button': '//*[@id="chips"]/ytmusic-chip-cloud-chip-renderer[1]/div/a/yt-icon/span/div',
    'first_song_item': '//*[@id="contents"]/ytmusic-responsive-list-item-renderer[1]',
    'song_title': '/div[2]/div[1]/yt-formatted-string/a',
    'song_artist_or_album': '/div[2]/div[3]/yt-formatted-string[1]/a',
    'triple_dot_menu': '//*[@id="contents"]/ytmusic-responsive-list-item-renderer[1]/ytmusic-menu-renderer',
    'share_button': '//yt-formatted-string[text() = "Share"]',
    'url_element': '//*[@id="share-url"]'
}

video_id_pattern = re.compile(r"v=([\w-]{11})")
word_pattern = re.compile(r"[\w'.]+")

driver = None

#returns the path to the 1st, 2nd, 3rd, (etc.) song on the searchlist. indexing starts at 1
def get_song_item_path(index):
    return xml_paths['first_song_item'][:-2] + str(index) + ']'

# compares words in first five songs to determine best match
def pick_best_song(desired_text): #TODO remove case sensitivity
    global driver
    desired_words = word_pattern.findall(desired_text)
    best_score = math.floor(len(desired_words) * 0.6) #the minimum score requirement is 60% of the highest score
    best_option = 1 #index of song

    for i in range(1,6):
        el_path = get_song_item_path(i)

        # get all the words in the options provided, including title, artists, and album text
        found_text = [driver.find_element(By.XPATH, el_path+xml_paths['song_title']).text]
        for el_thing in driver.find_elements(By.XPATH, el_path+xml_paths['song_artist_or_album']):
            found_text.append(el_thing.text)
        # create string of all the song info
        found_text = ' '.join(found_text)
        
        # rate score for matching words
        score = 0
        for word in desired_words:
            if word in found_text: score+=1
        if score == len(desired_words): # return early if perfect match is found
            return el_path
        elif score > best_score:
            best_score = score
            best_option = i

    return get_song_item_path(best_option)


def search_songs_with_Selenium(queryList):
    global driver
    output = []

    #countdown warning
    print('Launching web browser via Selenium in\n3')
    sleep(1)
    print('2')
    sleep(1)
    print('1')
    sleep(1)

    #initialize web driver
    driver = webdriver.Chrome()
    actions = ActionChains(driver)
    wait = WebDriverWait(driver, 5) # Wait for a maximum of 5 seconds

    for song in queryList:

        #convert to acceptable query for the url
        search_phrase = song.replace(' ', '+')
        driver.get(f"https://music.youtube.com/search?q={search_phrase}")

        #click song filter button
        song_filter_element = driver.find_element(By.XPATH, xml_paths['song_filter_button'])
        try:
            song_filter_element.click()
        except ElementNotInteractableException:
            sleep(1)
            song_filter_element.click()
        #wait for X button to load
        try:
            wait.until(expected_conditions.presence_of_element_located((By.XPATH, xml_paths['X_button'])))
        except Exception as e:
            raise Exception(f"Page failed to load songs filter before timeout on '{song}'.")
        # choose song based on how many words match
        selected_element = pick_best_song(song)
        selected_song = driver.find_element(By.XPATH, selected_element)
        #hover over the selected song
        actions.move_to_element(selected_song).perform()
        #click triple dot menu button
        triple_dot = driver.find_element(By.XPATH, xml_paths['triple_dot_menu'])
        try:
            triple_dot.click()
        except ElementNotInteractableException:
            sleep(1)
            triple_dot.click() #TODO fix the ElementNotInteractableException on this line. Occured on Handclap?
        #click share button
        share_element = driver.find_element(By.XPATH, xml_paths['share_button'])
        try:
            share_element.click()
        except ElementNotInteractableException:
            sleep(1)
            share_element.click()
        #wait until share url loads
        try:
            url_element = wait.until(expected_conditions.presence_of_element_located((By.XPATH, xml_paths['url_element'])))
        except Exception as e:
            print(f"Share url element for '{song}' not found before timeout: {e}")
        #get share url
        share_url = url_element.get_attribute("value")

        output.append(share_url)


    driver.quit()
    del driver
    #extract video IDs only, remove rest of url
    for i in range(len(output)):
        output[i] = video_id_pattern.search(output[i]).group(1)
    return output


#example:
if __name__ == "__main__":
    print(search_songs_with_Selenium(["Mr. Blue Sky", "Church Clap", "Mayonaise on an Escalator"]))