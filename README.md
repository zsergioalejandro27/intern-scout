# 🤖 InternScout

**Automated pipeline that scans European job boards and company career pages for software engineering internships and entry-level roles — and delivers real-time alerts straight to Telegram.**

Built as a personal tool to solve a very specific problem: manually checking dozens of job boards every day for internship opportunities in Europe is slow, repetitive, and easy to fall behind on. InternScout automates that search, filters out noise, and only surfaces what's actually relevant — new postings that fit the target roles, countries, and career stage.

---

## 🎯 What it does

- **Collects** internship, working-student, and graduate/entry-level software engineering postings from multiple sources (open job APIs, targeted scraping, and select company career pages).
- **Filters** by role relevance (excluding senior/lead positions), and by target geography — with priority on **Austria, Switzerland, and the Nordic countries**.
- **Tags** postings that mention visa sponsorship or support for international candidates, without discarding the rest.
- **Deduplicates** against previously seen postings using MongoDB, so you're only ever notified once per unique offer.
- **Notifies** instantly via a dedicated Telegram bot whenever a new, relevant posting is found.
- **Runs on a schedule** (several times a day) via GitHub Actions — no server to maintain, no manual runs required.

## 🧱 Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11+ |
| Database | MongoDB Atlas |
| Notifications | Telegram Bot API |
| Scheduling / CI | GitHub Actions (cron) |
| Scraping | `requests` + `BeautifulSoup` (and `Playwright` where needed for JS-heavy sites) |

## 🏗️ Architecture (high level)

```
GitHub Actions (cron, 4x/day)
        │
        ▼
   Collectors (APIs + scraping)
        │
        ▼
   Normalize → Filter → Tag
        │
        ▼
   Deduplicate (MongoDB, unique hash index)
        │
        ▼
   Notify new postings → Telegram
```

## 📌 Project Status

🚧 **Early development** — currently setting up the core pipeline (collector → database → notifier) with a single data source as a proof of concept, before expanding to additional sources and filters.

### Roadmap
- [ ] MVP: single source → MongoDB → Telegram (end-to-end)
- [ ] Additional job board integrations
- [ ] Targeted scraping for company career pages
- [ ] Role & geography filtering
- [ ] Visa sponsorship tagging
- [ ] Scheduled automation via GitHub Actions
- [ ] Error handling & run monitoring

## ⚙️ Setup

> Full setup instructions will be added once the MVP is functional.

Prerequisites will include:
- Python 3.11+
- A MongoDB Atlas cluster (free tier)
- A Telegram bot token (via [@BotFather](https://t.me/BotFather))

## 📄 License

MIT — feel free to fork and adapt for your own job search.

## 👤 About

Built by Sergio Alejandro Amaya Corzo — recent Software Engineering graduate, exploring internship and early-career opportunities across Europe. Connect on [LinkedIn](https://www.linkedin.com/in/sergio-alejandro-amaya-corzo-346077371) if you'd like to chat about the project or opportunities.