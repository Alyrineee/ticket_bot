from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Предложить идею"),
            KeyboardButton(text="Предложить новость"),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите вариант:",
)


async def inline_ban(id, msg_id):
    ban = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Забанить🔨", callback_data=f"ban_{id}"),
                InlineKeyboardButton(text="✅", callback_data=f"accept_{id}_{msg_id}"),
                InlineKeyboardButton(text="❌", callback_data=f"reject_{id}_{msg_id}"),
            ]
        ],
    )
    return ban
