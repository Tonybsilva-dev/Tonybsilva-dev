import os
import requests
from datetime import datetime

USERNAME = "SEU_USUARIO"
TOKEN = os.getenv("GITHUB_TOKEN")

def github_api(endpoint):
    url = f"https://api.github.com{endpoint}"
    r = requests.get(url, headers={"Authorization": f"token {TOKEN}"})
    r.raise_for_status()
    return r.json()

def fetch_projects():
    repos = github_api(f"/users/{USERNAME}/repos?sort=created&direction=desc")
    table = "| Nome | Stars | Link |\n|------|-------|------|\n"
    for repo in repos[:10]:
        table += f"| {repo['name']} | ⭐ {repo['stargazers_count']} | [Acessar]({repo['html_url']}) |\n"
    return table

def fetch_commits():
    events = github_api(f"/users/{USERNAME}/events")
    table = "| Repositório | Mensagem | Data |\n|-------------|----------|------|\n"
    count = 0
    for event in events:
        if event["type"] == "PushEvent":
            repo_name = event["repo"]["name"]
            for commit in event["payload"]["commits"]:
                msg = commit["message"].replace("|", "/")
                date_str = event["created_at"][:10]
                table += f"| {repo_name} | {msg} | {date_str} |\n"
                count += 1
                if count >= 15:
                    return table
    return table

def replace_between(content, start_tag, end_tag, replacement):
    start = content.find(start_tag) + len(start_tag)
    end = content.find(end_tag, start)
    return content[:start] + "\n" + replacement + "\n" + content[end:]

def update_readme():
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()

    projects_table = fetch_projects()
    commits_table = fetch_commits()

    readme = replace_between(readme, "<!--PROJECTS-->", "<!--PROJECTS-->", projects_table)
    readme = replace_between(readme, "<!--COMMITS-->", "<!--COMMITS-->", commits_table)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)

if __name__ == "__main__":
    update_readme()