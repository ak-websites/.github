import requests
import os
from datetime import datetime, timezone

ORG = "ak-websites"
TOKEN = os.environ.get("GITHUB_TOKEN", "")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
}

LANG_EMOJI = {
    "HTML": "🌐",
    "CSS": "🎨",
    "JavaScript": "⚡",
    "TypeScript": "⚡",
    "Vue": "💚",
    "React": "⚛️",
    "Python": "🐍",
    "PHP": "🐘",
    None: "📁",
}

SKIP_REPOS = {".github"}


def fetch_repos():
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/orgs/{ORG}/repos?per_page=100&page={page}&sort=updated"
        resp = requests.get(url, headers=HEADERS)
        resp.raise_for_status()
        data = resp.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    return repos


def status_badge(repo):
    updated = datetime.fromisoformat(repo["updated_at"].replace("Z", "+00:00"))
    days_ago = (datetime.now(timezone.utc) - updated).days
    if repo["archived"]:
        return "🗄️ Archived"
    elif repo.get("homepage"):
        return "🚀 Live"
    elif days_ago <= 14:
        return "🔨 In Progress"
    elif days_ago <= 90:
        return "🔧 Maintenance"
    else:
        return "📦 Stable"


def build_repo_table(repos):
    rows = []
    for repo in repos:
        if repo["name"] in SKIP_REPOS:
            continue
        name = repo["name"]
        url = repo["html_url"]
        homepage = repo.get("homepage") or ""
        desc = repo["description"] or "_No description provided._"
        lang = repo["language"]
        emoji = LANG_EMOJI.get(lang, "📁")
        lang_label = f"{emoji} {lang}" if lang else "📁 —"
        status = status_badge(repo)
        live_link = f"[🔗 Visit]({homepage})" if homepage else "—"
        rows.append(f"| [{name}]({url}) | {desc} | {lang_label} | {live_link} | {status} |")
    return "\n".join(rows)


def generate_readme(repos):
    table = build_repo_table(repos)
    total = len([r for r in repos if r["name"] not in SKIP_REPOS])
    updated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    readme = f"""<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&amp;color=gradient&amp;customColorList=2,6,30&amp;height=220&amp;section=header&amp;text=ak-websites&amp;fontSize=60&amp;fontColor=ffffff&amp;animation=fadeIn&amp;fontAlignY=38&amp;desc=A%20growing%20collection%20of%20websites%20%26%20web%20projects&amp;descAlignY=56&amp;descAlign=50" width="100%"/>

<p align="center">
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&amp;logo=html5&amp;logoColor=white"/>
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&amp;logo=css3&amp;logoColor=white"/>
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&amp;logo=javascript&amp;logoColor=black"/>
  <img src="https://img.shields.io/badge/React-61DAFB?style=for-the-badge&amp;logo=react&amp;logoColor=black"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Sites-{total}-blue?style=flat-square" />
  <img src="https://img.shields.io/badge/Focus-Web%20Development-blueviolet?style=flat-square" />
  <img src="https://img.shields.io/badge/Updated-{updated_at.replace(' ', '_').replace(':', '-')}-orange?style=flat-square" />
</p>

</div>

---

## 🌐 About This Organization

> **`ak-websites`** is a personal web development portfolio — a collection of websites, landing pages, and web projects built and maintained by Aashutosh Kuikel.

Each repository is a standalone web project with its own design, stack, and purpose. From simple landing pages to full web applications — this is where ideas go live.

---

## 📁 Projects ({total} sites)

| Repository | Description | Language | Live | Status |
|------------|-------------|----------|------|--------|
{table}

---

## 🛠 Tech Stack

| Layer | Tools |
|-------|-------|
| **Markup** | HTML5 |
| **Styling** | CSS3, Tailwind CSS |
| **Scripting** | JavaScript, TypeScript |
| **Frameworks** | React, Vue |
| **Hosting** | GitHub Pages, Vercel, Netlify |
| **Tools** | VS Code, Git, Figma |

---

## 🚀 Deployment

Most projects in this org are deployed via **GitHub Pages** or **Vercel**.
Live links are listed in the table above where available.

---

## 👤 Maintainer

<div align="center">

**Aashutosh Kuikel**

[![GitHub](https://img.shields.io/badge/GitHub-ak--websites-181717?style=for-the-badge&logo=github)](https://github.com/ak-websites)
[![ML Org](https://img.shields.io/badge/Also%20see-ak--Machine--Learning-blueviolet?style=for-the-badge&logo=github)](https://github.com/ak-Machine-Learning)
[![Location](https://img.shields.io/badge/📍-Kathmandu%2C%20Nepal-red?style=for-the-badge)]()

</div>

---

<div align="center">

_Last auto-updated: **{updated_at}**_ · _More sites incoming — watch this space._ 🌍

<img src="https://capsule-render.vercel.app/api?type=waving&amp;color=gradient&amp;customColorList=2,6,30&amp;height=100&amp;section=footer" width="100%"/>

</div>
"""
    return readme


def main():
    print("Fetching repos...")
    repos = fetch_repos()
    print(f"Found {len(repos)} repos.")

    readme = generate_readme(repos)

    os.makedirs("profile", exist_ok=True)
    with open("profile/README.md", "w", encoding="utf-8") as f:
        f.write(readme)

    print("✅ profile/README.md generated successfully.")


if __name__ == "__main__":
    main()
