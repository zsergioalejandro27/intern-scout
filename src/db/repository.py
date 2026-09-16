from datetime import datetime, timezone

from pymongo.errors import DuplicateKeyError

from src.db.mongo_client import jobs_collection


def insert_if_new(job_doc: dict) -> bool:
    try:
        jobs_collection.insert_one(job_doc)
        return True
    except DuplicateKeyError:
        return False


def mark_notified(job_hash: str) -> None:
    jobs_collection.update_one(
        {"job_hash": job_hash},
        {"$set": {"notified": True, "notified_at": datetime.now(timezone.utc)}},
    )
