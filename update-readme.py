import requests
import os
from datetime import datetime, timezone

GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "SEU_USUARIO")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

API_URL = "https://api.github.com/graphql"

def run_query(query, variables=None):
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    response = requests.post(API_URL, json={"query": query, "variables": variables}, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Erro na API: {response.status_code} - {response.text}")
    return response.json()

def fetch_commit_count_today():
    """Retorna quantos commits foram feitos hoje."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%dT00:00:00Z")

    query = """
    query($username:String!, $from:DateTime!) {
      user(login: $username) {
        contributionsCollection(from: $from) {
          totalCommitContributions
        }
      }
    }
    """
    data = run_query(query, {"username": GITHUB_USERNAME, "from": today})
    return data["data"]["user"]["contributionsCollection"]["totalCommitContributions"]

def fetch_github_stats():
    """Retorna estatísticas gerais do GitHub."""
    query = """
    query($username:String!) {
      user(login: $username) {
        repositories {
          totalCount
        }
        pullRequests {
          totalCount
        }
        issues {
          totalCount
        }
        contributionsCollection {
          totalCommitContributions
        }
      }
    }
    """
    data = run_query(query, {"username": GITHUB_USERNAME})
    user = data["data"]["user"]

    return {
        "total_repos": user["repositories"]["totalCount"],
        "total_prs": user["pullRequests"]["totalCount"],
        "total_issues": user["issues"]["totalCount"],
        "total_commits": user["contributionsCollection"]["totalCommitContributions"]
    }

def update_readme(commit_today, stats):
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()

    readme = replace_section(readme, "commit_status", [
        f"- 📅 Commits hoje: **{commit_today}**"
    ])

    readme = replace_section(readme, "github_stats", [
        f"- 📦 Repositórios: **{stats['total_repos']}**",
        f"- 🔀 Pull Requests: **{stats['total_prs']}**",
        f"- 🐛 Issues: **{stats['total_issues']}**",
        f"- 📝 Commits totais: **{stats['total_commits']}**"
    ])

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)

def replace_section(content, marker, lines):
    start_marker = f"<!--START_SECTION:{marker}-->"
    end_marker = f"<!--END_SECTION:{marker}-->"
    start_index = content.find(start_marker)
    end_index = content.find(end_marker)

    if start_index == -1 or end_index == -1:
        raise ValueError(f"Marcadores {marker} não encontrados no README.md")

    start_index += len(start_marker)
    return content[:start_index] + "\n" + "\n".join(lines) + "\n" + content[end_index:]

if __name__ == "__main__":
    if not GITHUB_TOKEN:
        raise Exception("Defina a variável de ambiente GITHUB_TOKEN")

    commits_today = fetch_commit_count_today()
    stats = fetch_github_stats()
    update_readme(commits_today, stats)
    print(f"[{datetime.now()}] README.md atualizado.")