import hashlib, subprocess, os
from os.path import isfile
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

import tgbot

urlx = 'https://allstar.gg/u/k1nkiller'

def parse_links10(url):
    driver = webdriver.Chrome()
    driver.implicitly_wait(3)

    driver.maximize_window()
    driver.get(url)
    raw_videos_list = driver.find_elements(by=By.CSS_SELECTOR, value=".sc-AxjAm.sc-AxirZ.sc-jCDoaw.hZRXae")
    sleep(3)
    links = []
    for x in raw_videos_list:
        driver.execute_script("arguments[0].scrollIntoView();", x)
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", x)
        sleep(1)
        video_element_link = driver.find_element(by=By.CSS_SELECTOR, value=".vjs-tech").get_attribute("src")
        links.append(video_element_link)
    driver.close()
    return links

def check_for_new_clips(links: list):
    links_new = []
    if not isfile("data\\links.txt"):
        links_new = links
    else:
        with open("data\\links.txt", "r") as f:
            links_old = f.readlines()
        for link in links:
            if link not in links_old:
                links_new.append(link)
    with open("data\\links.txt", "a") as f:
        for x in links_new:
            f.write(x + "\n")
    return links_new

def download(links: list):
    output_folder = "data\\videos"
    os.makedirs(output_folder, exist_ok=True)
    print(links)
    for link in links:
        file_name = "highlight" + hashlib.md5(link.encode()).hexdigest() + ".mp4"
        output_path = os.path.join(output_folder, file_name)
        try:
            subprocess.run(["curl", "-L", "-o", output_path, link], check=True)
            print(f"Saved as: {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")

# download(check_for_new_clips(parse_links10(urlx)))
for video in os.listdir("data\\videos"):
    tgbot.video_spam(video)