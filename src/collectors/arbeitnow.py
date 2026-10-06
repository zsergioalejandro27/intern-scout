from datetime import datetime, timezone

import requests

from src.collectors.base import Collector, RawPosting
from src.processing.geo import detect_country

API_URL = "https://www.arbeitnow.com/api/job-board-api"


class ArbeitnowCollector(Collector):
    name = "arbeitnow"

    def fetch(self) -> list[RawPosting]:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        return [self._to_posting(raw) for raw in response.json()["data"]]

    def _to_posting(self, raw: dict) -> RawPosting:
        location = raw.get("location")
        return RawPosting(
            source=self.name,
            title=raw["title"],
            company=raw["company_name"],
            url=raw["url"],
            description=raw["description"],
            location=location,
            country=detect_country(location),
            posted_at=datetime.fromtimestamp(raw["created_at"], tz=timezone.utc),
        )
