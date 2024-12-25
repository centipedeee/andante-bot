import asyncio
import hashlib, subprocess, os
from os.path import isfile
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

from src import tgbot
BASE_DIR, LINKS_FILE_PATH, VIDEOS_DIR_PATH, USERS_FILE_PATH = '', '', '', ''

def main():
    global BASE_DIR, LINKS_FILE_PATH, VIDEOS_DIR_PATH, USERS_FILE_PATH
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    LINKS_FILE_PATH = os.path.join(BASE_DIR, "links")
    VIDEOS_DIR_PATH = os.path.join(BASE_DIR, "videos")
    USERS_FILE_PATH = os.path.join(BASE_DIR, "users")
    asyncio.run(start_crt(os.getenv('LINKS').split(',')))


async def start_crt(urls: list[str]):
    while True:
        for url in urls:
            start_parser_sequence(url)
            with open(USERS_FILE_PATH, "r") as f:
                users = f.read().split('\n')
            await send_videos(users)
        await asyncio.sleep(1800)

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

    if not isfile(LINKS_FILE_PATH):
        links_new = links
    else:
        with open(LINKS_FILE_PATH, "r") as f:
            links_old = f.read().splitlines()
        for link in links:
            if link not in links_old:
                links_new.append(link)

    with open(LINKS_FILE_PATH, "a") as f:
        for x in links_new:
            f.write(x + "\n")

    return links_new


def download(links: list):
    os.makedirs(VIDEOS_DIR_PATH, exist_ok=True)
    print(links)

    for link in links:
        file_name = "highlight" + hashlib.md5(link.encode()).hexdigest() + ".mp4"
        output_path = os.path.join(VIDEOS_DIR_PATH, file_name)
        try:
            subprocess.run(["curl", "-L", "-o", output_path, link], check=True)
            print(f"Saved as: {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
    return


def start_parser_sequence(url):
    download(check_for_new_clips(parse_links10(url)))
    return


async def send_videos(users):
    for video in os.listdir(VIDEOS_DIR_PATH):
        video_path = os.path.join(VIDEOS_DIR_PATH, video)
        for each in users:
            try:
                print(f"Отправка видео {video} пользователю {each}")
                await tgbot.video_newsletter(each, video_path)
            except Exception as e:
                print(f"Ошибка отправки {video} пользователю {each}: {e}")
        os.remove(video_path)





if __name__ == "__main__":
    load_dotenv()
    admins = os.getenv('ADMINS').split(',')
    asyncio.run(send_videos(admins))


