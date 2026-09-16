import requests

API_URL = "https://www.arbeitnow.com/api/job-board-api"


def fetch_jobs() -> list[dict]:
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()
    return response.json()["data"]
