import asyncio

from telegram import Bot

from src.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


def send_job_notification(job: dict) -> None:
    message = (
        f"🆕 {job['title']}\n"
        f"{job['company']} — {job.get('location', 'N/A')}\n"
        f"{job['url']}"
    )
    asyncio.run(_send(message))


async def _send(message: str) -> None:
    async with Bot(token=TELEGRAM_BOT_TOKEN) as bot:
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
