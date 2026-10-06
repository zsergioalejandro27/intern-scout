import asyncio
import html

from telegram import Bot

from src.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


def send_job_notification(job: dict) -> None:
    title = html.escape(job["title"])
    company = html.escape(job["company"])
    location = html.escape(job.get("location") or "N/A")
    snippet = html.escape(job.get("description_snippet") or "")
    url = html.escape(job["url"], quote=True)
    source = html.escape(job.get("source") or "N/A")

    message = (
        f"🆕 <b>{title}</b>\n"
        f"🏢 {company} — 📍 {location}\n\n"
        f"{snippet}...\n\n"
        f'🔗 <a href="{url}">Ver oferta</a>\n'
        f"🌐 Fuente: {source}"
    )
    asyncio.run(_send(message))


async def _send(message: str) -> None:
    async with Bot(token=TELEGRAM_BOT_TOKEN) as bot:
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode="HTML")
