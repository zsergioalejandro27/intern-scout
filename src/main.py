import argparse

from src.collectors.arbeitnow import fetch_jobs
from src.db.repository import insert_if_new, mark_notified
from src.notifier.telegram_bot import send_job_notification
from src.processing.normalizer import normalize_arbeitnow_job


def run(seed: bool = False) -> None:
    raw_jobs = fetch_jobs()
    new_count = 0

    for raw_job in raw_jobs:
        job = normalize_arbeitnow_job(raw_job)
        if not insert_if_new(job):
            continue

        new_count += 1
        if not seed:
            send_job_notification(job)
        mark_notified(job["job_hash"])

    label = "sembrados (sin notificar)" if seed else "nuevos notificados"
    print(f"Jobs revisados: {len(raw_jobs)} | {label}: {new_count}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", action="store_true", help="Guarda las ofertas actuales sin enviar notificaciones")
    args = parser.parse_args()
    run(seed=args.seed)
