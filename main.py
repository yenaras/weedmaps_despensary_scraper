#!/usr/bin/env python3
from state_list import states
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
import csv


def main():
    driver = load_driver()
    url = "https://weedmaps.com/dispensaries/in/united-states/"
    driver.get(url)

    dispensaries = []

    # iterate each state
    for state in states:
        driver.get(url + state)
        print(f"Scraping {state}")

        # wait til element present, and grab all the dispensaries on page
        div_elements = WebDriverWait(driver, 30).until(
            lambda x: x.find_elements(
                By.CLASS_NAME,
                "region-subregions-tray__ListItem-sc-hfrdvw-3.wwvEB"))

        # grab the name and link of each dispensary
        for div_element in div_elements:
            dispensary_tag = div_element.find_element(By.TAG_NAME, 'a')
            dispensary_dict = {"name": dispensary_tag.get_attribute('aria-label'),
                               "link": dispensary_tag.get_attribute('href')}

            # append the dispensary to the list if it's not already in the list
            if dispensary_dict not in dispensaries:
                dispensaries.append(dispensary_dict)
    print(dispensaries)
    with open("despensaries.csv", "w") as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow(["name", "link"])
        for dispensary in dispensaries:
            writer.writerow(dispensary.values())


def load_driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--ignore-certificate-errors")
    driver = webdriver.Chrome(options=chrome_options)
    return driver


if __name__ == "__main__":
    main()
