import asyncio

from telegram import Bot

from src.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

_bot = Bot(token=TELEGRAM_BOT_TOKEN)


def send_job_notification(job: dict) -> None:
    message = (
        f"🆕 {job['title']}\n"
        f"{job['company']} — {job.get('location', 'N/A')}\n"
        f"{job['url']}"
    )
    asyncio.run(_bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message))
