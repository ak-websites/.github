import requests
import os
from datetime import datetime, timezone

ORG = "ak-Machine-Learning"
TOKEN = os.environ.get("GITHUB_TOKEN", "")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
}

LANG_EMOJI = {
    "Python": "🐍",
    "Jupyter Notebook": "📓",
    "JavaScript": "🌐",
    "TypeScript": "🌐",
    "R": "📊",
    "Shell": "⚙️",
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
    elif days_ago <= 14:
        return "✅ Active"
    elif days_ago <= 90:
        return "🔨 In Progress"
    else:
        return "🧪 Experimental"


def build_repo_table(repos):
    rows = []
    for repo in repos:
        if repo["name"] in SKIP_REPOS:
            continue
        name = repo["name"]
        url = repo["html_url"]
        desc = repo["description"] or "_No description provided._"
        lang = repo["language"]
        emoji = LANG_EMOJI.get(lang, "📁")
        lang_label = f"{emoji} {lang}" if lang else "📁 —"
        status = status_badge(repo)
        rows.append(f"| [{name}]({url}) | {desc} | {lang_label} | {status} |")
    return "\n".join(rows)


def generate_readme(repos):
    table = build_repo_table(repos)
    total = len([r for r in repos if r["name"] not in SKIP_REPOS])
    updated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    readme = f"""<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&amp;color=gradient&amp;customColorList=12,14,20&amp;height=220&amp;section=header&amp;text=ak-Machine-Learning&amp;fontSize=52&amp;fontColor=ffffff&amp;animation=fadeIn&amp;fontAlignY=38&amp;desc=A%20collection%20of%20ML%20%26%20AI%20projects%20built%20from%20scratch&amp;descAlignY=56&amp;descAlign=50" width="100%"/>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&amp;logo=python&amp;logoColor=white"/>
  <img src="https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&amp;logo=jupyter&amp;logoColor=white"/>
  <img src="https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&amp;logo=tensorflow&amp;logoColor=white"/>
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&amp;logo=scikit-learn&amp;logoColor=white"/>
  <img src="https://img.shields.io/badge/NLP-8A2BE2?style=for-the-badge&amp;logo=openai&amp;logoColor=white"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Repos-{total}-brightgreen?style=flat-square" />
  <img src="https://img.shields.io/badge/Focus-ML%20%7C%20NLP%20%7C%20AI-blue?style=flat-square" />
  <img src="https://img.shields.io/badge/Updated-{updated_at.replace(' ', '_').replace(':', '-')}-orange?style=flat-square" />
</p>

</div>

---

## 🧠 About This Organization

> **`ak-Machine-Learning`** is a personal ML research & project organization — a growing collection of experiments, classifiers, deep learning models, and AI tools built hands-on from the ground up.

Each repository is an independent project with its own dataset, pipeline, and goal. This is not a single project — it's an evolving portfolio.

---

## 📁 Repositories ({total} projects)

| Repository | Description | Language | Status |
|------------|-------------|----------|--------|
{table}



---

## 🔬 Core Focus Areas

```
Natural Language Processing (NLP)
   ├── Text Classification
   ├── Sentiment Analysis
   ├── Review Rating Prediction
   └── Chatbot Development

Machine Learning
   ├── Classical Models  (Naive Bayes, SVM, Logistic Regression)
   ├── Ensemble Methods  (Random Forest, Gradient Boosting)
   └── Deep Learning     (LSTM, GRU, Neural Networks)

ML Engineering
   ├── Pipeline Design (leakage-free, modular)
   ├── Model Evaluation (F1, AUC-ROC, Confusion Matrix)
   └── Experiment Tracking & Comparison
```

---

## 🛠 Tech Stack

| Layer | Tools |
|-------|-------|
| **Language** | Python 3.10+ |
| **Notebooks** | Jupyter Notebook, Google Colab |
| **ML / Classical** | scikit-learn, XGBoost |
| **Deep Learning** | TensorFlow, Keras |
| **NLP** | NLTK, TF-IDF, Word Embeddings |
| **Data** | NumPy, Pandas |
| **Visualization** | Matplotlib, Seaborn, Plotly |
| **Version Control** | Git, GitHub |

---

## 👤 Maintainer

<div align="center">

**Aashutosh Kuikel**

<a href="https://github.com/ak-Machine-Learning"><img src="https://img.shields.io/badge/GitHub-ak--Machine--Learning-181717?style=for-the-badge&amp;logo=github&amp;logoColor=white"/></a>
<a href=""><img src="https://img.shields.io/badge/📍-Kathmandu%2C%20Nepal-red?style=for-the-badge"/></a>

</div>

---

<div align="center">

_Last auto-updated: **{updated_at}**_ · _More projects incoming — watch this space._ 👀

<img src="https://capsule-render.vercel.app/api?type=waving&amp;color=gradient&amp;customColorList=12,14,20&amp;height=100&amp;section=footer" width="100%"/>

</div>
"""
    return readme


def main():
    print("Fetching repos...")
    repos = fetch_repos()
    print(f"Found {len(repos)} repos.")

    readme = generate_readme(repos)

    # Write to profile/README.md (org profile location)
    os.makedirs("profile", exist_ok=True)
    with open("profile/README.md", "w", encoding="utf-8") as f:
        f.write(readme)

    print("✅ profile/README.md generated successfully.")


if __name__ == "__main__":
    main()
