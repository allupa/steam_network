from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import re

"""
Collects the review scores.
To use, create an empty json file "review_scores.json" with an empty json object {}
:param profile: the profile name (might be different from ID64)
:param driver: chromedriver
:param steamID64: the profile steamID64
"""
def crawl_review_score(profile, driver, steamID64):
    driver.get(f'https://steamcommunity.com/id/{profile}/recommended/')
    src = driver.page_source
    sorry_found = re.search(r'The specified profile could not be found', src)
    sorry_finnish = re.search(r'Pahoittelumme!', src)
    # Profile not found with id
    try:
        if(sorry_found == None and sorry_finnish == None):
            reviews = driver.find_elements_by_xpath("//div[@class='review_box']/div[@class='header']")
            score = 0
            for n in reviews:
                score += parse_review(n.text)
            write_to_review_score({steamID64: score})
        else:
            driver.get(f'https://steamcommunity.com/profiles/{steamID64}/recommended/')
            reviews = driver.find_elements_by_xpath("//div[@class='review_box']/div[@class='header']")
            score = 0
            for n in reviews:
                score += parse_review(n.text)
            write_to_review_score({steamID64: score})
    except Exception as e:
        print(e)


def write_to_review_score(data):
    with open('review_scores.json') as json_file:
        existing_data = json.load(json_file)
        existing_data.update(data)
    with open('review_scores.json', 'w') as f:
        json.dump(existing_data, f)

def parse_review(review):
    lines = review.split('\n')
    score = 0
    for l in lines:
        splitted = l.split(' ')
        for n in splitted:
            score += int(n) if n.isnumeric() else 0
    return score
        
