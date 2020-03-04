from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import xml.etree.ElementTree as ET
import time
import csv
import re
import util
import json


# Remove double spaces, whitespaces and change everything to uppercase from ski data
def clean_ski(l):
    for r in l:
        r = r.strip()
        re.sub(' {2,}', ' ', r)
    csv_l = [r.upper().split() for r in l]
    return csv_l


# Initialize chrome webdriver
def get_chrome_driver(config):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument("--incognito")
    exec_path = config['chrome-webdriver']['windows']
    driver = webdriver.Chrome(options=options, executable_path=exec_path)
    return driver


def write_to_csv(lines):
    with open('results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(lines)


def write_to_json(data):
    with open('results.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)


def crawl_friends(profile, driver):
    driver.get(f'https://steamcommunity.com/id/{profile}/friends/')
    elements = driver.find_elements_by_class_name("friend_block_v2")
    friends = [i.get_attribute("data-steamid") for i in elements]
    return friends


def get_steam_id(element, driver):
    profile_link = element.text.split('/')[4]
    driver.get(f'https://steamcommunity.com/id/{profile_link}?xml=1')
    root = ET.fromstring(driver.page_source)
    for i in root.iter('steamID64'):
        steamID64 = i.text  # The first ID encountered
    return steamID64


def main():
    config = util.load_config()
    driver = get_chrome_driver(config)
    data = {}
    # Open reviews and pick first review to start crawling
    driver.get("https://steamcommunity.com/?subsection=reviews")
    print(driver.title)

    # Locate submit button, click to get all results
    driver.implicitly_wait(15)
    reviewCards = driver.find_elements_by_class_name("apphub_Card")
    reviewCards[1].click() # Mod as needed, some profiles are private
    element = driver.find_element_by_xpath("//a[contains(@href, 'steamcommunity.com/id')]")
    profile_link = element.text.split('/')[4]
    steamID64 = get_steam_id(element, driver)
    print("Writing to csv...")
    data[steamID64] = crawl_friends(profile_link, driver)
    write_to_json(data)
    time.sleep(10)
    # Close everything
    driver.quit()
    return 0


if __name__ == '__main__':
    main()
