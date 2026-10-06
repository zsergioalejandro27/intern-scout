import hashlib
from datetime import datetime, timezone

from bs4 import BeautifulSoup

from src.collectors.base import RawPosting

SNIPPET_LENGTH = 300


def normalize(posting: RawPosting, role_type: str) -> dict:
    job_hash = hashlib.sha256(
        f"{posting.title}{posting.company}{posting.url}".encode("utf-8")
    ).hexdigest()
    description_text = BeautifulSoup(posting.description, "html.parser").get_text(" ", strip=True)

    return {
        "job_hash": job_hash,
        "title": posting.title,
        "company": posting.company,
        "location": posting.location,
        "country": posting.country,
        "role_type": role_type,
        "source": posting.source,
        "url": posting.url,
        "description_snippet": description_text[:SNIPPET_LENGTH],
        "posted_date": posting.posted_at,
        "scraped_at": datetime.now(timezone.utc),
        "notified": False,
    }
