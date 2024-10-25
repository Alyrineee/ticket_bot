import sqlite3

from aiogram import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable
from aiogram.types import TelegramObject, Message

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()


class BanMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        user_id = event.from_user.id
        check_user = cursor.execute(
            f"SELECT id FROM bans WHERE id={user_id}"
        ).fetchone()
        if event.chat.type == "private":
            if check_user:
                return await event.answer("Извини, ты в бане : (\n\nРазабан: @FondyEzh")
            return await handler(event, data)
