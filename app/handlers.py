import sqlite3
import random

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
admins = [1711546279, 5253078721]

class TicketsState(StatesGroup):
    idea = State()
    news = State()
    reject = State()



@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Тут ты можешь предложить идею",
        reply_markup=kb.main,
    )


@router.message(F.text == "Предложить идею")
async def meet(message: Message, state: FSMContext):
    await state.set_state(TicketsState.idea)
    await message.answer(
        "Привет! Напиши ниже идею, которую хочешь реализовать в нашей школе. "
        "Помни о правилах фильтрации через которые будет проходить твоя идея:\n"
        "Адекватность – идея должна быть разумной и выполнимой.\n"
        "Реализуемость – она должна быть практической в рамках школы.\n"
        "Необходимость - если идея проходит через первичные фильтры, то она публикуется в наш открытый телеграм-канал, где проходит голосование о необходимости ее реализации.\n"
        "За отправку неприличных и подобных идей администратор имеет право вас заблокировать."
    )


@router.message(F.text == "Предложить новость")
async def meet(message: Message, state: FSMContext):
    await state.set_state(TicketsState.news)
    await message.answer(
        "Здесь вы можете публиковать важные и официальные новости от учителей, а также другие актуальные события школьной жизни.\n"
        "Пожалуйста, придерживайтесь строгой серьезности в сообщениях: за публикацию несоответствующего контента предусмотрен бан."
    )


@router.message(TicketsState.idea)
@router.message(TicketsState.news)
async def query_state(message: Message, state: FSMContext):
    msg_id = random.randint(0, 100000000)
    type_of_query = "Новое обращение"
    current_state = await state.get_state()
    if current_state == TicketsState.news:
        admins.append(807240611)
        type_of_query = "Новая новость"
    for admin_id in admins:
        try:
            if message.text:
                await state.clear()
                await message.bot.send_message(
                    admin_id,
                    f"{type_of_query} от {message.chat.id} "
                    f"(@{str(message.chat.username) + ', ' + str(message.chat.first_name) + ' ' + str(message.chat.last_name)})\n\n"
                    + str(message.text),
                    reply_markup=await kb.inline_ban(message.chat.id, msg_id),
                )
            elif message.photo and message.caption:
                await state.clear()
                await message.bot.send_photo(
                    admin_id,
                    message.photo[-1].file_id,
                    caption=f"{type_of_query}  от "
                    f"{message.chat.id} "
                    f"(@{str(message.chat.username) + ', ' + str(message.chat.first_name) + ' ' + str(message.chat.last_name)})\n\n"
                    + message.caption,
                    reply_markup=await kb.inline_ban(message.chat.id, msg_id),
                )
            else:
                await message.reply("Разрешен только текст или фото с текстом")
                break
        except:
            print("Skipping...")
    await message.answer(f"Сообщение #{msg_id} отправлено!")


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
    if callback.from_user.id in admins:
        try:
            if int(callback.data.split("_")[1]) != 5253078721:
                await callback.answer("Ты забанил юзера", show_alert=True)
                cursor.execute(
                    f"INSERT INTO bans VALUES " f"({int(callback.data.split('_')[1])})"
                )
                conn.commit()
            else:
                await callback.answer("Его нельзя забанить", show_alert=True)
        except:
            await callback.answer("Юзер уже в бане", show_alert=True)

    else:
        await callback.answer("У тебя нет прав", show_alert=True)


@router.callback_query(F.data.split("_")[0] == "accept")
async def inline_accept(callback: CallbackQuery):
    await callback.answer()
    await callback.bot.send_message(
        callback.data.split("_")[1],
        f"Привет, твою идею #{callback.data.split("_")[2]} одобрили!",
    )


@router.callback_query(F.data.split("_")[0] == "reject")
async def inline_reject_first(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(msg_id=callback.data.split("_")[2], user_id=callback.data.split("_")[1])
    await state.set_state(TicketsState.reject)
    await callback.bot.send_message(callback.message.chat.id, "Напиши причину отказа")


@router.message(TicketsState.reject)
async def inline_reject_second(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.bot.send_message(
        data["user_id"],
        f"Привет, твою идею #{data["msg_id"]} отклонили: (\n\n"
            f"Причина: {message.text}"
    )
    await state.clear()
