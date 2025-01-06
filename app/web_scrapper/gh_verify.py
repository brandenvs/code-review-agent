import requests
import json


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
