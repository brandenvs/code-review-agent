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


def fetch_github_directory(student_id, task_name, github_token):
    base_url = "https://api.github.com/repos/hyperiondev-bootcamps"
    git_url = f"{base_url}/{student_id}/contents/{task_name}"
    
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {github_token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    try:
        response = requests.get(git_url, headers=headers)
        
        # Print detailed error information
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {json.dumps(dict(response.headers), indent=2)}")
        
        if response.status_code == 404:
            print("Repository or path not found")
            print(f"Attempted URL: {git_url}")
            return None
            
        elif response.status_code == 403:
            print("Authentication failed or rate limit exceeded")
            print(f"Rate Limit Remaining: {response.headers.get('X-RateLimit-Remaining')}")
            return None
            
        elif response.status_code != 200:
            print(f"Error response: {response.text}")
            return None
            
        # Success case
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None


def check_repo_access(student_id, github_token):
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {github_token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    repo_url = f"https://api.github.com/repos/hyperiondev-bootcamps/{student_id}"
    response = requests.get(repo_url, headers=headers)
    
    print(f"Repository check status: {response.status_code}")
    if response.status_code == 200:
        print("Repository is accessible")
    else:
        print(f"Repository issue: {response.text}")


def check_token(github_token):
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {github_token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    response = requests.get("https://api.github.com/user", headers=headers)
    print(f"Token check status: {response.status_code}")
    if response.status_code == 200:
        print("Token is valid and has access")
        print(f"Scopes: {response.headers.get('X-OAuth-Scopes')}")
    else:
        print(f"Token issue: {response.text}")


def list_repo_contents(student_id, github_token):
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {github_token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    contents_url = f"https://api.github.com/repos/hyperiondev-bootcamps/{student_id}/contents"
    response = requests.get(contents_url, headers=headers)
    
    if response.status_code == 200:
        print("\nAvailable contents:")
        for item in response.json():
            print(f"{item['path']}")
    else:
        print(f"Could not list contents: {response.text}")


if __name__ == "__main__":
    edge_driver_path = os.path.join(BASE_DIR, 'webDriver', 'msedgedriver.exe')

    driver = get_webdriver(edge_driver_path)
    
    html_file_path = os.path.join(BASE_DIR, 'index.html')

    file_url = f"file:///{html_file_path}"

    review_data_list = load_review_data(file_url, driver)

    for i, review_data in enumerate(review_data_list):
        driver = get_webdriver(edge_driver_path)

        if i == 10:
            break
            

        if review_data['course_lvl'] == 'DFEDSL1':
            review_text = get_review(review_data['review_link'], driver)

            git_url = f'https://api.github.com/repos/hyperiondev-bootcamps/{review_data["student_id"]}/contents/{review_data["task_name"]}'

            local_base_path = os.path.join(BASE_DIR.parent, 'data', review_data["task_name"], review_data["student_id"])

            download_github_content(git_url, local_base_path, GITHUB_TOKEN)

            local_base_path_review = os.path.join(BASE_DIR.parent, 'data', review_data["task_name"], review_data["student_id"], 'review_text.txt')

            with open(local_base_path_review, "w", encoding="utf-8") as file:
                file.write(review_text)

    try:
        driver.close()
        driver.quit()

    except Exception as ex:
        print('Driver already closed and quitted!', ex)
