# 🤖 InternScout

**Automated pipeline that scans European job boards for software engineering internships and entry-level roles — and delivers real-time alerts straight to Telegram.**

Built as a personal tool to solve a very specific problem: manually checking job boards every day for internship opportunities in Europe is slow, repetitive, and easy to fall behind on. InternScout automates that search, filters out noise, and only surfaces what's actually relevant.

**Status: 🟢 Live** — running in production since September 2026, checking for new postings every 6 hours with zero manual intervention.

---

## 🎯 What it does

- **Fetches** software engineering postings from [Arbeitnow](https://www.arbeitnow.com/api/job-board-api)'s open job board API.
- **Filters** for relevance: software/engineering roles at internship, working-student, junior, or entry-level seniority — excluding senior/lead/staff/principal positions and unrelated fields (marketing, design, research, etc.).
- **Deduplicates** against previously seen postings using MongoDB (unique hash index), so you're only ever notified once per unique offer.
- **Notifies** instantly via a dedicated Telegram bot whenever a new, relevant posting is found.
- **Runs on a schedule** (every 6 hours) via GitHub Actions — no server to maintain, no manual runs required.

## 🧱 Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11+ |
| Database | MongoDB Atlas (free M0 tier) |
| Notifications | Telegram Bot API (`python-telegram-bot`) |
| Scheduling / CI | GitHub Actions (cron) |
| HTTP / parsing | `requests` + `BeautifulSoup` (cleans HTML out of job descriptions) |

## 🏗️ Architecture

```
GitHub Actions (cron, every 6h)
        │
        ▼
   Fetch (Arbeitnow API)
        │
        ▼
   Normalize + Filter (role/seniority keywords)
        │
        ▼
   Deduplicate (MongoDB, unique hash index)
        │
        ▼
   Notify new postings → Telegram
```

## 📌 Project Status & Roadmap

- [x] MVP: single source (Arbeitnow) → MongoDB → Telegram, end-to-end
- [x] Role & seniority filtering (software + entry-level, excluding senior roles)
- [x] Scheduled automation via GitHub Actions (every 6h)
- [ ] Geographic filtering (priority on Austria, Switzerland, Nordic countries)
- [ ] Additional job board integrations (Adzuna next — also an open API)
- [ ] Targeted scraping for company career pages / other boards (Karriere.at, Stepstone)
- [ ] Visa sponsorship tagging
- [ ] Automated tests

See [DEVLOG.md](DEVLOG.md) for the full build history, decisions, and bugs fixed along the way.

## ⚙️ Setup

Prerequisites:
- Python 3.11+
- A [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register) cluster (free M0 tier)
- A Telegram bot token (create one via [@BotFather](https://t.me/BotFather))

```bash
git clone https://github.com/zsergioalejandro27/intern-scout.git
cd intern-scout
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows PowerShell — use .venv/bin/activate on macOS/Linux
pip install -e .
```

Copy `.env.example` to `.env` and fill in your own credentials:

```
MONGO_URI=mongodb+srv://<user>:<password>@<cluster>.mongodb.net/?appName=Cluster0
TELEGRAM_BOT_TOKEN=<your bot token>
TELEGRAM_CHAT_ID=<your telegram chat id>
```

Run it once manually:

```bash
python -m src.main
```

To run automatically on a schedule, fork this repo and add `MONGO_URI`, `TELEGRAM_BOT_TOKEN`, and `TELEGRAM_CHAT_ID` as GitHub Secrets (Settings → Secrets and variables → Actions) — the included workflow (`.github/workflows/scrape.yml`) handles the rest. Make sure your MongoDB Atlas cluster's Network Access allows `0.0.0.0/0`, since GitHub Actions runners don't have a fixed IP.

## 📄 License

MIT — feel free to fork and adapt for your own job search.

## 👤 About

Built by Sergio Alejandro Amaya Corzo — recent Software Engineering graduate, exploring internship and early-career opportunities across Europe. Connect on [LinkedIn](https://www.linkedin.com/in/sergio-alejandro-amaya-corzo-346077371) if you'd like to chat about the project or opportunities.
