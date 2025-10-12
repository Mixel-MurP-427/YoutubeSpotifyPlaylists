#This function is an alternative to using the Youtube API to search for music.
#It uses Selenium to open https://music.youtube.com/ and manually search for songs

import json
import re
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By


#constants
xml_paths = {
#   'searchbar': '//*[@id="input"]',
    'song_filter_button': '//yt-formatted-string[text() = "Songs"]',
    'X_button': '//*[@id="chips"]/ytmusic-chip-cloud-chip-renderer[1]/div/a/yt-icon/span/div',
    'first_song_item': '//*[@id="contents"]/ytmusic-responsive-list-item-renderer[1]',
    'triple_dot_menu': '//*[@id="contents"]/ytmusic-responsive-list-item-renderer[1]/ytmusic-menu-renderer',
    'share_button': '//yt-formatted-string[text() = "Share"]',
    'url_element': '//*[@id="share-url"]'
}

video_id_pattern = re.compile(r"v=([\w-]{11})")


def search_songs_with_Selenium(queryList):
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
        song_filter_element.click()
        #wait for X button to load
        try:
            unaccessed_var = wait.until(expected_conditions.presence_of_element_located((By.XPATH, xml_paths['X_button'])))
        except Exception as e:
            raise Exception(f"Page failed to load songs filter before timeout on '{song}'.")
        #hover over first song on list
        first_song = driver.find_element(By.XPATH, xml_paths['first_song_item'])
        actions.move_to_element(first_song).perform()
        #click triple dot menu button
        triple_dot = driver.find_element(By.XPATH, xml_paths['triple_dot_menu'])
        triple_dot.click()
        #click share button
        share_element = driver.find_element(By.XPATH, xml_paths['share_button'])
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
    #extract video IDs only, remove rest of url
    for i in range(len(output)):
        output[i] = video_id_pattern.search(output[i]).group(1)
    return output


#example:
if __name__ == "__main__":
    print(search_songs_with_Selenium(["Mr. Blue Sky", "Church Clap", "Mayonaise on an Escalator"]))