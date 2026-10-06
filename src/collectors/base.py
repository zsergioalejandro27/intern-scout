from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass
class RawPosting:
    source: str
    title: str
    company: str
    url: str
    description: str
    location: str | None = None
    country: str | None = None
    posted_at: datetime | None = None


class Collector(ABC):
    name: str

    @abstractmethod
    def fetch(self) -> list[RawPosting]:
        ...
