from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

import requests
from urllib.parse import quote
import base64
from urllib.parse import unquote
import json

import requests
import os
from pathlib import Path

from scrap_reviews import load_review_data, get_review
from decouple import config


BASE_DIR = Path(__file__).resolve().parent

ENV_PATH = os.path.join(BASE_DIR, '.env')

config._find_file(ENV_PATH)
GITHUB_TOKEN = config('GITHUB_TOKEN')


def get_webdriver(exe_path) -> webdriver.Edge:
    options = Options()
    edge_service = Service(exe_path)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"

    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("referer=https://www.google.com/")
    options.add_argument("accept-language=en-US,en;q=0.9")

    driver = webdriver.Edge(service=edge_service)
    return driver


def download_github_content(content_url, local_path, github_token):
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {github_token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    response = requests.get(content_url, headers=headers)
    if response.status_code == 200:
        content = response.json()
        if isinstance(content, list):
            # It's a directory
            os.makedirs(local_path, exist_ok=True)
            for item in content:
                item_path = os.path.join(local_path, item['name'])
                if item['type'] == 'dir':
                    download_github_content(item['url'], item_path, github_token)
                else:
                    download_github_file(item['download_url'], item_path, github_token)
        else:
            # It's a file
            file_content = base64.b64decode(content['content'])
            with open(local_path, 'wb') as file:
                file.write(file_content)
            print(f"Downloaded: {local_path}")
    else:
        print(f"Failed to fetch content: {response.status_code}")


def download_github_file(download_url, local_path, github_token):
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {github_token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    response = requests.get(download_url, headers=headers)
    if response.status_code == 200:
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        with open(local_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {local_path}")
    else:
        print(f"Failed to download {local_path}: {response.status_code}")


if __name__ == "__main__":
    edge_driver_path = os.path.join(BASE_DIR, 'webDriver', 'msedgedriver.exe')

    driver = get_webdriver(edge_driver_path)
    
    html_file_path = os.path.join(BASE_DIR, 'index.html')

    file_url = f"file:///{html_file_path}"

    review_data_list = load_review_data(file_url, driver)

    for i, review_data in enumerate(review_data_list):
        if review_data['course_lvl'] == 'DFECSL1':
            git_url = f'https://api.github.com/repos/hyperiondev-bootcamps/{review_data["student_id"]}/contents/{review_data["task_name"]}'

            print(git_url)
            print(f'---\nGetting {review_data["student_id"]} Data from GitHub\n---')

            local_base_path = os.path.join(BASE_DIR.parent, 'data', review_data["student_id"], review_data["task_name"])

            download_github_content(git_url, local_base_path, GITHUB_TOKEN)

            print('Saving to ...', local_base_path)
            print('------')

            print('---\nGetting Review Data\n---')
            print(review_data['task_name'])
            print('------')

            driver = get_webdriver(edge_driver_path)
            review_text = get_review(review_data['review_link'], driver)

            local_base_path_review = os.path.join(BASE_DIR.parent, 'data', review_data["student_id"], review_data["task_name"], 'review_text.txt')

            with open(local_base_path_review, "w", encoding="utf-8") as file:
                file.write(review_text)

    try:
        driver.close()
        driver.quit()

    except Exception as ex:
        print('Driver already closed and quitted!', ex)
