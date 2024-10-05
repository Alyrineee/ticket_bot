import sqlite3
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import CommandStart, Command
import app.keyboard as kb
from app.middlewares import BanMiddleware

router = Router()
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()
router.message.outer_middleware(BanMiddleware())


class TicketsState(StatesGroup):
    query = State()
    glasses = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Тут ты можешь предложить идею или сообщить о нехватке стаканчиков",
        reply_markup=kb.main,
    )


@router.message(F.text == "Предложить идею")
async def meet(message: Message, state: FSMContext):
    await state.set_state(TicketsState.query)
    await message.answer(
        "Привет! Напиши ниже идею, которую хочешь реализовать в нашей школе. "
        "Помни о правилах фильтрации через которые будет проходить твоя идея:\n"
        "- Адекватность\n"
        "- Возможность\n"
        "- Необходимость\n"
        "За отправку неприличных и подобных идей администратор имеет право вас заблокировать."
    )


@router.message(F.text == "Сообщить о нехватке стаканчиков")
async def glasses(message: Message, state: FSMContext):
    await state.set_state(TicketsState.glasses)
    await message.answer(
        "Привет! Если ты нашел кулер без стаканчиков, "
        "скинь фото их отсутствия и где находится кулер.\n"
        "За отправку ложных или не связанных с опцией сведений "
        "администратор имеет право вас заблокировать."
    )


@router.message(TicketsState.glasses)
async def glasses_state(message: Message, state: FSMContext):
    if message.photo and message.caption:
        await message.bot.send_photo(
            "-1002189126528",
            message.photo[-1].file_id,
            caption=f"Новое обращение от "
                    f"{message.chat.id} "
                    f"(@{str(message.chat.username) + ', ' + str(message.chat.first_name) + ' ' + str(message.chat.last_name)})\n\n"
                    + message.caption,
            reply_markup=await kb.inline_ban(message.chat.id),
        )
        await state.clear()
    else:
        await message.reply("Разрешены только картинки c текстом")


@router.message(TicketsState.query)
async def query_state(message: Message, state: FSMContext):
    if message.text:
        await message.bot.send_message(
            "1711546279",
            f"Новое обращение от {message.chat.id} "
            f"(@{str(message.chat.username) + ', ' + str(message.chat.first_name) + ' ' + str(message.chat.last_name)})\n\n"
            + str(message.text),
            reply_markup=await kb.inline_ban(message.chat.id),
        )
        await state.clear()
    else:
        await message.reply("Разрешен только текст")


@router.message(Command("ban"))
async def ban(message: Message):
    if message.chat.id == 5253078721 or message.chat.id == 1711546279:
        cursor.execute(f"INSERT INTO bans VALUES ({message.text.split()[1]})")
        conn.commit()
        await message.reply("Пользователь забанен")


@router.message(Command("unban"))
async def unban(message: Message):
    if message.chat.id == 5253078721 or message.chat.id == 1711546279:
        cursor.execute(f"DELETE FROM bans WHERE ({message.text.split()[1]})")
        conn.commit()
        await message.reply("Пользователь pазбанен")


@router.callback_query(F.data.split("_")[0] == "ban")
async def inline_ban(callback: CallbackQuery):
    if callback.from_user.id == 5253078721 or callback.from_user.id == 1711546279:
        await callback.answer("Ты забанил юзера", show_alert=True)
        try:
            await callback.answer("Ты забанил юзера", show_alert=True)
            cursor.execute(
                f"INSERT INTO bans VALUES ({int(callback.data.split('_')[1])})"
            )
            conn.commit()
        except:
            await callback.answer("Юзер уже в бане", show_alert=True)

    else:
        await callback.answer("У тебя нет прав", show_alert=True)
