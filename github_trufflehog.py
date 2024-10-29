import requests
import subprocess
import os
from dotenv import load_dotenv # type: ignore

load_dotenv()
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# Replace with your GitHub API token
ORGANIZATION = 'apple'  # Change this to the desired organization
API_URL = f'https://api.github.com/orgs/{ORGANIZATION}/repos'

headers = {
    "Authorization": f"token {GITHUB_TOKEN}"
}

def get_repositories():
    repos = []
    page = 1
    while True:
        response = requests.get(API_URL, headers=headers, params={"page": page, "per_page": 100})
        data = response.json()
        if not data:
            break
        repos.extend([repo['html_url'] for repo in data])
        page += 1
    return repos

def save_repositories_to_file(repos, filename="org_repos.txt"):
    with open(filename, 'w') as file:
        for repo in repos:
            file.write(repo + "\n")

def scan_with_trufflehog(repo_url):
    print(f"Scanning {repo_url} with TruffleHog...")
    subprocess.run(["trufflehog", "github", "--repo", repo_url, "--only-verified"])

def main():
    repos = get_repositories()
    save_repositories_to_file(repos)  # Save all repos to org_repos.txt
    for repo in repos:
        scan_with_trufflehog(repo)

if __name__ == "__main__":
    main()
