from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Сообщить о нехватке стаканчиков"),
            KeyboardButton(text="Предложить идею"),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите вариант:",
)


async def inline_ban(id):
    ban = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Забанить", callback_data=f"ban_{id}")]
        ],
    )
    return ban
