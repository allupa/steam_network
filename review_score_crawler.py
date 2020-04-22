from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

def crawl_review_score(profile, driver):
    driver.get(f'https://steamcommunity.com/id/{profile}/recommended/')
    reviews = driver.find_elements_by_xpath("//div[@class='review_box']/div[@class='header']")
    score = 0
    for n in reviews:
        score += parse_review(n.text)
    write_to_review_score({"joni": score})

def write_to_review_score(data):
    with open('review_scores.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)

def parse_review(review):
    lines = review.split('\n')
    score = 0
    for l in lines:
        splitted = l.split(' ')
        for n in splitted:
            print(f'evaluating {n} to {n.isnumeric()}')
            score += int(n) if n.isnumeric() else 0
    return score
        
