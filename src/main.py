import argparse

from src.collectors.arbeitnow import ArbeitnowCollector
from src.collectors.base import Collector
from src.db.repository import insert_if_new, mark_notified
from src.notifier.telegram_bot import send_job_notification
from src.processing.filters import classify_role
from src.processing.geo import TARGET_COUNTRIES
from src.processing.normalizer import normalize

COLLECTORS: list[Collector] = [ArbeitnowCollector()]


def run(seed: bool = False) -> None:
    failed_sources = []

    for collector in COLLECTORS:
        try:
            postings = collector.fetch()
        except Exception as error:
            print(f"[{collector.name}] ERROR: {error}")
            failed_sources.append(collector.name)
            continue

        in_target_count = 0
        relevant_count = 0
        new_count = 0

        for posting in postings:
            if posting.country not in TARGET_COUNTRIES:
                continue
            in_target_count += 1

            role_type = classify_role(posting.title)
            if role_type is None:
                continue
            relevant_count += 1

            job = normalize(posting, role_type)
            if not insert_if_new(job):
                continue

            new_count += 1
            if not seed:
                send_job_notification(job)
            mark_notified(job["job_hash"])

        label = "sembrados (sin notificar)" if seed else "nuevos notificados"
        print(
            f"[{collector.name}] revisados: {len(postings)} | en paises objetivo: {in_target_count} | "
            f"relevantes: {relevant_count} | {label}: {new_count}"
        )

    if failed_sources:
        raise SystemExit(f"Fuentes con error: {', '.join(failed_sources)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", action="store_true", help="Guarda las ofertas actuales sin enviar notificaciones")
    args = parser.parse_args()
    run(seed=args.seed)
