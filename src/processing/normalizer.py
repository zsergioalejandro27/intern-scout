import hashlib
from datetime import datetime, timezone

from bs4 import BeautifulSoup

SNIPPET_LENGTH = 300


def normalize_arbeitnow_job(raw_job: dict) -> dict:
    title = raw_job["title"]
    company = raw_job["company_name"]
    url = raw_job["url"]

    job_hash = hashlib.sha256(f"{title}{company}{url}".encode("utf-8")).hexdigest()
    description_text = BeautifulSoup(raw_job["description"], "html.parser").get_text(" ", strip=True)

    return {
        "job_hash": job_hash,
        "title": title,
        "company": company,
        "location": raw_job.get("location"),
        "source": "arbeitnow",
        "url": url,
        "description_snippet": description_text[:SNIPPET_LENGTH],
        "posted_date": datetime.fromtimestamp(raw_job["created_at"], tz=timezone.utc),
        "scraped_at": datetime.now(timezone.utc),
        "notified": False,
    }
