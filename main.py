import logging
import os
import sqlite3
from datetime import datetime

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

SUPPORT_USERNAME = "gwjeh"
ADMIN_USER_ID = [5091594841, 5142322536, 5172170861]

bot = Bot(token="7785027084:AAG7xbLlmuloH5DpYipjW8UZR8_Zq8gUhR8")
dp = Dispatcher()

conn = sqlite3.connect('steam_shop.db')
cursor = conn.cursor()


def create_tables():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        balance INTEGER DEFAULT 0,
        username TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS games (
        game_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        genre TEXT NOT NULL,
        login TEXT,
        password TEXT,
        is_used BOOLEAN DEFAULT 0,
        price INTEGER NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cart (
        cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        game_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (user_id),
        FOREIGN KEY (game_id) REFERENCES games (game_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS support_tickets (
        ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        message TEXT NOT NULL,
        created_at TEXT NOT NULL,
        status TEXT DEFAULT 'open',
        FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    conn.commit()


create_tables()


def populate_games_data():
    cursor.execute("SELECT COUNT(*) FROM games")
    count = cursor.fetchone()[0]

    if count == 0:
        games_data = [
            ("Prototype 2", "Action", "rwgran1", "wet444wed", 199),
            ("Alan Wake", "Horror", "rwgran1", "wet444wed", 199),
            ("Paint the Town Red", "Action", "rzm745", "Rzm85770923", 149),
            ("Grand Theft Auto IV: The Complete Edition", "Action", "rzm745", "Rzm85770923", 149),
            ("Tropico 6", "Strategy", "liyagarcueva97", "CxvMhK9dPkUaIb", 199),
            ("GTA VICE CITY", "Action", "alp21cm", "10306969970aA", 99),
            ("ELDEN RING", "RPG", "Thragg_767", "ev8Z5YyvY42RmiX", 199),
            ("Resident Evil 4 Remake", "Horror", "bejdw24074", "https://steamkk.com", 199),
            ("Far cry 3", "Action", "youallsuck_911", "Adje2003a.1", 199),
            ("BLACK MYTH: WUKONG DELUX", "Action", "mario_wukong", "QCP7PFHMW4VV", 199),
            ("Cyberpunk 2077", "RPG", "icpropenin1988", "siski33Fh845X3BYiBLZyb1987", 199),
            ("Resident Evil Village", "Horror", "nikintolya92", "aJMpnB9GtONAyY1Q", 149),
            ("Far Cry 5", "Action", "dr4xon22", "ZIa_B--Z", 149),
            ("Assassin's Creed Chronicles India", "Adventure", "kxzoi70142", "VkY5EauB", 149),
            ("Assassin's Creed Chronicles China", "Adventure", "kxzoi70142", "VkY5EauB", 149),
            ("Assassin's Creed Chronicles Russia", "Adventure", "kxzoi70142", "VkY5EauB", 149),
            ("Assassin's Creed Brotherhood", "Action", "kxzoi70142", "VkY5EauB", 99),
            ("Mortal Combat X", "Fighting", "leo3d3", "tricolor231002", 199),
            ("Lords of the Fallen Deluxe Edition", "RPG", "rkwoh77645", "uofh08187V", 149),
            ("Call Of Duty WW2", "Shooter", "brbba2063", "che600220", 149),
            ("Dead Cells", "Roguelike", "hsrp18939", "3HjumZTz334I", 149),
            ("Five Nights at Freddy's Security Breach", "Horror", "nojevik__0", "wwe123456", 149),
            ("Borderlands 3", "Shooter", "ivy_wreathh", "yT1ML3YWe3dw52x", 199),
            ("Fallout 4", "RPG", "swfushe4", "Sw654247", 149),
            ("GTA 4", "Action", "wqm322495", "ac7QPfa3", 199),
            ("Assassin's creed 3 Remastered", "Action", "junjun888666733", "Xiaohejiaoao78965", 149),
            ("Resident Evil 7 Biohazard", "Horror", "jocuriargenrinia", "70Games.net92", 199),
            ("cuphead", "Platformer", "su0wn1hf", "UOipTT58vG5XZ1", 149),
            ("LITTLE NIGHTMARES", "Horror", "DecorousThoughtlessWhale", "Weirdmice91", 99),
            ("maneater", "Action", "yrij69325", "xmp8eADW", 199),
            ("Alien Isolation", "Horror", "jiaoaohehe188940", "junyi1139908", 149),
            ("tomb raider", "Adventure", "KickeyGame33", "I81PJDWCAS341FA", 149),
            ("kingdom Come: deliverance II", "RPG", "phvmg47604", "bfmjj99570", 199),
            ("Call of Duty: Modern Warfare 2 (2009)", "Shooter", "dimkoxd", "Dimko1995", 199),
            ("Terraria", "Sandbox", "charizardkingg", "Ronnie-13", 99),
            ("Slime Rancher", "Simulation", "charizardkingg", "Ronnie-13", 149),
            ("Age of Empires III: Definitive Edition", "Strategy", "komski01", "omarca06", 99),
            ("Watch Dogs Legion", "Action", "Bt5Pd3Zm9Sz4", "Yk2Ho8Wl5Im2", 199),
            ("hollow knight", "Metroidvania", "niodev", "funpay.onibist.users.5871937", 149),
            ("Need For Speed Heat", "Racing", "rd5977", "951753852.ACHU", 149),
            ("hotline miami", "Action", "keraoff", "v,!86QZSG(<e6:<", 99),
            ("Stray", "Adventure", "wbtq1088322", "steamok4566H", 99),
            ("Prototype", "Action", "axelturba3660", "monster3660", 149),
            ("HEARTS OF IRON IV", "Strategy", "meteprotr", "3D88ASX2AMCG", 99),
            ("Mortal Kombat 11", "Fighting", "kintygabobs1981", "XIdg5JiQZ11978", 149),
            ("Warhammer 40,000: Space Marine 2", "Action", "willianphillips7u", "mwe8p9SO4y1998", 299),
            ("EA SPORTS FC 25", "Sports", "neifreebzapme1973", "2y6rS0eJ6v2000", 199),
            ("Metro exodus", "Shooter", "chriswest6k", "xgfb9z5s", 149),
            ("Metro last light redux", "Shooter", "chriswest6k", "xgfb9z5s", 149),
            ("metro 2033 redux", "Shooter", "chriswest6k", "xgfb9z5s", 149),
            ("resident evil 2", "Horror", "lthNoviokv1", "hxrTV21zqgpkRuAnTAY0", 149),
            ("frostpunk 2", "Strategy", "lkzra09777", "siski33FpndvDpZ066475", 199),
            ("Dead Island 2", "Action", "cbkse74345", "siski33BYkJWT6HiZM7lhirtXsk", 199),
            ("God of war", "Action", "jmyhtrPtaosv1", "siski33hkFpEiHgWvccQV", 199),
            ("spider man remastered", "Action", "josephlighting98", "STEAM_ACCOUNT_64DVFndjei397421", 299),
            ("the last of us part 1", "Adventure", "tijodeme1978", "v0329fETm71987", 199)
        ]

        cursor.executemany(
            "INSERT INTO games (title, genre, login, password, price) VALUES (?, ?, ?, ?, ?)",
            games_data
        )
        conn.commit()


populate_games_data()


class AddBalanceState(StatesGroup):
    amount = State()


class SupportState(StatesGroup):
    message = State()


class AddGameStates(StatesGroup):
    waiting_for_genre = State()
    waiting_for_title = State()
    waiting_for_price = State()
    waiting_for_login = State()
    waiting_for_password = State()


class EditGameStates(StatesGroup):
    waiting_for_new_price = State()


@dp.message(Command("add_game"))
async def add_game_command(message: types.Message, state: FSMContext):
    if message.from_user.id not in ADMIN_USER_ID:
        await message.answer("⛔ У вас нет прав для выполнения этой команды")
        return

    cursor.execute("SELECT DISTINCT genre FROM games")
    genres = [genre[0] for genre in cursor.fetchall()]

    builder = InlineKeyboardBuilder()
    for genre in genres:
        builder.add(InlineKeyboardButton(text=genre, callback_data=f"add_genre_{genre}"))
    builder.add(InlineKeyboardButton(text="➕ Новый жанр", callback_data="add_new_genre"))
    builder.add(InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_add_game"))
    builder.adjust(2)

    await message.answer(
        "🎮 Добавление новой игры\n\n"
        "Выберите жанр игры:",
        reply_markup=builder.as_markup()
    )
    await state.set_state(AddGameStates.waiting_for_genre)


@dp.callback_query(F.data.startswith("add_genre_"))
async def genre_selected_for_add(callback: types.CallbackQuery, state: FSMContext):
    genre = callback.data.split("_")[2]
    await state.update_data(genre=genre)
    await callback.message.edit_text(f"Выбран жанр: {genre}\n\nВведите название игры:")
    await state.set_state(AddGameStates.waiting_for_title)
    await callback.answer()


@dp.callback_query(F.data == "add_new_genre")
async def new_genre_selected(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите название нового жанра:")
    await state.set_state(AddGameStates.waiting_for_genre)
    await callback.answer()


@dp.message(AddGameStates.waiting_for_genre)
async def new_genre_received(message: types.Message, state: FSMContext):
    genre = message.text.strip()
    await state.update_data(genre=genre)
    await message.answer(f"Новый жанр: {genre}\n\nВведите название игры:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddGameStates.waiting_for_title)


@dp.message(AddGameStates.waiting_for_title)
async def game_title_received(message: types.Message, state: FSMContext):
    title = message.text.strip()
    await state.update_data(title=title)
    await message.answer("Введите цену игры (в рублях):")
    await state.set_state(AddGameStates.waiting_for_price)


@dp.message(AddGameStates.waiting_for_price)
async def game_price_received(message: types.Message, state: FSMContext):
    try:
        price = int(message.text)
        if price <= 0:
            raise ValueError
        await state.update_data(price=price)
        await message.answer("Введите логин для игры:")
        await state.set_state(AddGameStates.waiting_for_login)
    except ValueError:
        await message.answer("❌ Пожалуйста, введите корректную цену (целое число больше 0):")


@dp.message(AddGameStates.waiting_for_login)
async def game_login_received(message: types.Message, state: FSMContext):
    login = message.text.strip()
    await state.update_data(login=login)
    await message.answer("Введите пароль для игры:")
    await state.set_state(AddGameStates.waiting_for_password)


@dp.message(AddGameStates.waiting_for_password)
async def game_password_received(message: types.Message, state: FSMContext):
    password = message.text.strip()
    data = await state.get_data()

    try:
        cursor.execute(
            "INSERT INTO games (title, genre, login, password, price) VALUES (?, ?, ?, ?, ?)",
            (data['title'], data['genre'], data['login'], password, data['price'])
        )
        conn.commit()

        await message.answer(
            f"✅ Игра успешно добавлена в базу данных!\n\n"
            f"🎮 Название: {data['title']}\n"
            f"📁 Жанр: {data['genre']}\n"
            f"💵 Цена: {data['price']}₽\n"
            f"👤 Логин: {data['login']}\n"
            f"🔑 Пароль: {password}"
        )
        logger.info(f"Admin added new game: {data['title']}")
    except Exception as e:
        await message.answer(f"❌ Ошибка при добавлении игры: {e}")
        logger.error(f"Error adding game: {e}")

    await state.clear()


@dp.callback_query(F.data == "cancel_add_game")
async def cancel_add_game(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("❌ Добавление игры отменено")
    await callback.answer()


def get_main_menu_kb():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="🕹️ Каталог игр", callback_data="catalog"),
        InlineKeyboardButton(text="🛒 Корзина", callback_data="cart"),
        InlineKeyboardButton(text="💰 Баланс", callback_data="balance"),
        InlineKeyboardButton(text="💳 Пополнить баланс", callback_data="add_balance"),
        InlineKeyboardButton(text="🆘 Техподдержка", callback_data="support"),
    )
    builder.adjust(2, 2, 1)
    return builder.as_markup()


def get_support_kb():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Написать в поддержку", callback_data="write_to_support"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")
    )
    builder.adjust(1)
    return builder.as_markup()


def get_genres_kb():
    cursor.execute("SELECT DISTINCT genre FROM games")
    genres = cursor.fetchall()

    builder = InlineKeyboardBuilder()
    for genre in genres:
        builder.add(InlineKeyboardButton(text=genre[0], callback_data=f"genre_{genre[0]}"))
    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu"))
    builder.adjust(2)
    return builder.as_markup()


def get_games_by_genre_kb(genre):
    cursor.execute("SELECT game_id, title, price FROM games WHERE genre = ? AND is_used = 0", (genre,))
    games = cursor.fetchall()

    builder = InlineKeyboardBuilder()
    for game in games:
        builder.add(InlineKeyboardButton(text=f"{game[1]} - {game[2]}₽", callback_data=f"game_{game[0]}"))
    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="catalog"))
    builder.adjust(1)
    return builder.as_markup()


def get_game_details_kb(game_id, in_cart=False, is_admin=False):
    builder = InlineKeyboardBuilder()
    if not in_cart:
        builder.add(InlineKeyboardButton(text="🛒 Добавить в корзину", callback_data=f"add_to_cart_{game_id}"))
    else:
        builder.add(InlineKeyboardButton(text="❌ Удалить из корзины", callback_data=f"remove_from_cart_{game_id}"))

    if is_admin:
        builder.add(InlineKeyboardButton(text="✏️ Редактировать цену", callback_data=f"edit_price_{game_id}"))
        builder.add(InlineKeyboardButton(text="🗑️ Удалить игру", callback_data=f"admin_delete_game_{game_id}"))

    builder.add(InlineKeyboardButton(
        text="🔙 Назад",
        callback_data=f"genre_{cursor.execute('SELECT genre FROM games WHERE game_id = ?', (game_id,)).fetchone()[0]}"
    ))
    builder.adjust(1)
    return builder.as_markup()


@dp.callback_query(F.data.startswith("admin_delete_game_"))
async def admin_delete_game(callback: types.CallbackQuery):
    if callback.from_user.id not in ADMIN_USER_ID:
        await callback.answer("⛔ У вас нет прав для выполнения этого действия")
        return

    game_id = int(callback.data.split("_")[3])

    cursor.execute("SELECT title FROM games WHERE game_id = ?", (game_id,))
    game_title = cursor.fetchone()[0]

    confirm_kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Да, удалить", callback_data=f"confirm_delete_{game_id}"),
            InlineKeyboardButton(text="❌ Нет, отмена", callback_data=f"game_{game_id}")
        ]
    ])

    await callback.message.edit_text(
        f"⚠️ Вы уверены, что хотите удалить игру '{game_title}'?\n\n"
        "Это действие нельзя отменить!",
        reply_markup=confirm_kb
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("confirm_delete_"))
async def confirm_delete_game(callback: types.CallbackQuery):
    if callback.from_user.id not in ADMIN_USER_ID:
        await callback.answer("⛔ У вас нет прав для выполнения этого действия")
        return

    game_id = int(callback.data.split("_")[2])

    cursor.execute("SELECT title FROM games WHERE game_id = ?", (game_id,))
    game_title = cursor.fetchone()[0]

    try:
        cursor.execute("DELETE FROM games WHERE game_id = ?", (game_id,))
        cursor.execute("DELETE FROM cart WHERE game_id = ?", (game_id,))
        conn.commit()

        await callback.message.edit_text(
            f"✅ Игра '{game_title}' успешно удалена из базы данных",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text="🔙 В каталог", callback_data="catalog")
            ]])
        )
        logger.info(f"Admin deleted game: {game_title}")
    except Exception as e:
        await callback.message.edit_text(
            f"❌ Ошибка при удалении игры: {e}",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text="🔙 Назад", callback_data=f"game_{game_id}")
            ]])
        )
        logger.error(f"Error deleting game: {e}")

    await callback.answer()


@dp.callback_query(F.data.startswith("edit_price_"))
async def edit_price_start(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id not in ADMIN_USER_ID:
        await callback.answer("⛔ У вас нет прав для выполнения этого действия")
        return

    game_id = int(callback.data.split("_")[2])
    await state.update_data(game_id=game_id)

    cursor.execute("SELECT title, price FROM games WHERE game_id = ?", (game_id,))
    game = cursor.fetchone()

    await callback.message.edit_text(
        f"✏️ Редактирование цены игры:\n\n"
        f"🎮 {game[0]}\n"
        f"💵 Текущая цена: {game[1]}₽\n\n"
        f"Введите новую цену:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="🔙 Отмена", callback_data=f"game_{game_id}")
        ]])
    )
    await state.set_state(EditGameStates.waiting_for_new_price)
    await callback.answer()


@dp.message(EditGameStates.waiting_for_new_price)
async def save_new_price(message: types.Message, state: FSMContext):
    try:
        new_price = int(message.text)
        if new_price <= 0:
            raise ValueError
    except ValueError:
        await message.answer("❌ Пожалуйста, введите корректную цену (целое число больше 0):")
        return

    data = await state.get_data()
    game_id = data['game_id']

    cursor.execute("UPDATE games SET price = ? WHERE game_id = ?", (new_price, game_id))
    conn.commit()

    cursor.execute("SELECT title FROM games WHERE game_id = ?", (game_id,))
    game_title = cursor.fetchone()[0]

    await message.answer(
        f"✅ Цена игры '{game_title}' успешно изменена на {new_price}₽",
        reply_markup=get_main_menu_kb()
    )
    await state.clear()

    cursor.execute("SELECT title, genre, price FROM games WHERE game_id = ?", (game_id,))
    game = cursor.fetchone()

    cursor.execute("SELECT 1 FROM cart WHERE user_id = ? AND game_id = ?", (message.from_user.id, game_id))
    in_cart = bool(cursor.fetchone())

    text = (
        f"🎮 <b>{game[0]}</b>\n\n"
        f"📝 Жанр: <i>{game[1]}</i>\n\n"
        f"💵 Цена: <b>{game[2]}₽</b>"
    )

    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id - 1,
        text=text,
        reply_markup=get_game_details_kb(game_id, in_cart, True),
        parse_mode='HTML'
    )


def get_cart_kb(user_id):
    cursor.execute('''
    SELECT g.game_id, g.title, g.price 
    FROM cart c 
    JOIN games g ON c.game_id = g.game_id 
    WHERE c.user_id = ?
    ''', (user_id,))
    games = cursor.fetchall()

    builder = InlineKeyboardBuilder()
    for game in games:
        builder.add(InlineKeyboardButton(text=f"{game[1]} - {game[2]}₽", callback_data=f"cart_game_{game[0]}"))

    if games:
        builder.add(InlineKeyboardButton(text="💵 Купить", callback_data="buy"))
        builder.add(InlineKeyboardButton(text="❌ Очистить корзину", callback_data="clear_cart"))

    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu"))
    builder.adjust(1)
    return builder.as_markup()


def get_cart_game_kb(game_id):
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="❌ Удалить из корзины", callback_data=f"remove_from_cart_{game_id}"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="cart")
    )
    builder.adjust(1)
    return builder.as_markup()


def get_balance_kb():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="💳 Пополнить баланс", callback_data="add_balance"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")
    )
    builder.adjust(1)
    return builder.as_markup()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username

    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)",
        (user_id, username)
    )
    conn.commit()

    logger.info(f"User {user_id} (@{username}) started the bot")

    await message.answer(
        "🎮 Добро пожаловать в магазин Steam игр!\n\n"
        "Здесь вы можете купить игры для Steam по выгодным ценам.",
        reply_markup=get_main_menu_kb()
    )


@dp.callback_query(F.data == "support")
async def support(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🆘 Техническая поддержка\n\n"
        f"Если у вас возникли проблемы, вы можете:\n"
        f"1. Написать нам в поддержку через бота\n"
        f"2. Связаться напрямую: @{SUPPORT_USERNAME}",
        reply_markup=get_support_kb()
    )
    await callback.answer()


@dp.callback_query(F.data == "write_to_support")
async def write_to_support(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "✉️ Опишите вашу проблему, и мы постараемся помочь как можно скорее:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="🔙 Отмена", callback_data="support")
        ]])
    )
    await state.set_state(SupportState.message)
    await callback.answer()


@dp.message(SupportState.message)
async def process_support_message(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    support_message = message.text
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        "INSERT INTO support_tickets (user_id, message, created_at) VALUES (?, ?, ?)",
        (user_id, support_message, created_at)
    )
    conn.commit()

    logger.info(f"New support ticket from user {user_id}: {support_message}")

    try:
        for i in ADMIN_USER_ID:
            await bot.send_message(
                i,
                f"🆘 Новый запрос в поддержку\n\n"
                f"👤 Пользователь: @{message.from_user.username or 'нет username'}\n"
                f"🆔 ID: tg://user?id={user_id} - {user_id}\n"
                f"📝 Сообщение:\n{support_message}"
            )
    except Exception as e:
        logger.error(f"Failed to send support message to admin: {e}")

    await message.answer(
        "✅ Ваше сообщение отправлено в поддержку. Мы ответим вам в ближайшее время.\n"
        f"Вы также можете связаться напрямую: @{SUPPORT_USERNAME}",
        reply_markup=get_main_menu_kb()
    )
    await state.clear()


@dp.callback_query(F.data == "main_menu")
async def main_menu(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🎮 Главное меню магазина Steam игр",
        reply_markup=get_main_menu_kb()
    )
    await callback.answer()


@dp.callback_query(F.data == "catalog")
async def catalog(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🎮 Выберите жанр игры:",
        reply_markup=get_genres_kb()
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("genre_"))
async def genre_selected(callback: types.CallbackQuery):
    genre = callback.data.split("_")[1]
    await callback.message.edit_text(
        f"🎮 Игры в жанре {genre}:",
        reply_markup=get_games_by_genre_kb(genre)
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("game_"))
async def game_selected(callback: types.CallbackQuery):
    game_id = int(callback.data.split("_")[1])
    cursor.execute("SELECT title, genre, price FROM games WHERE game_id = ?", (game_id,))
    game = cursor.fetchone()

    cursor.execute("SELECT 1 FROM cart WHERE user_id = ? AND game_id = ?", (callback.from_user.id, game_id))
    in_cart = bool(cursor.fetchone())

    text = (
        f"🎮 <b>{game[0]}</b>\n\n"
        f"📝 Жанр: <i>{game[1]}</i>\n\n"
        f"💵 Цена: <b>{game[2]}₽</b>"
    )

    is_admin = callback.from_user.id in ADMIN_USER_ID

    await callback.message.edit_text(
        text,
        reply_markup=get_game_details_kb(game_id, in_cart, is_admin),
        parse_mode='HTML'
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("add_to_cart_"))
async def add_to_cart(callback: types.CallbackQuery):
    game_id = int(callback.data.split("_")[3])
    user_id = callback.from_user.id

    cursor.execute("SELECT 1 FROM cart WHERE user_id = ? AND game_id = ?", (user_id, game_id))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO cart (user_id, game_id) VALUES (?, ?)", (user_id, game_id))
        conn.commit()
        await callback.answer("✅ Игра добавлена в корзину!")
    else:
        await callback.answer("ℹ️ Эта игра уже в вашей корзине")


@dp.callback_query(F.data.startswith("remove_from_cart_"))
async def remove_from_cart(callback: types.CallbackQuery):
    game_id = int(callback.data.split("_")[3])
    user_id = callback.from_user.id

    cursor.execute("DELETE FROM cart WHERE user_id = ? AND game_id = ?", (user_id, game_id))
    conn.commit()

    cursor.execute("SELECT title, genre, price FROM games WHERE game_id = ?", (game_id,))
    game = cursor.fetchone()

    text = (
        f"🎮 <b>{game[0]}</b>\n\n"
        f"📝 Жанр: <i>{game[1]}</i>\n\n"
        f"💵 Цена: <b>{game[2]}₽</b>"
    )

    await callback.message.edit_text(
        text,
        reply_markup=get_game_details_kb(game_id, False),
        parse_mode='HTML'
    )
    await callback.answer("❌ Игра удалена из корзины")


@dp.callback_query(F.data == "cart")
async def show_cart(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    cursor.execute('''
    SELECT g.title, g.price 
    FROM cart c 
    JOIN games g ON c.game_id = g.game_id 
    WHERE c.user_id = ?
    ''', (user_id,))
    games = cursor.fetchall()

    if games:
        total = sum(game[1] for game in games)
        text = "🛒 Ваша корзина:\n\n" + "\n".join(
            [f"🎮 {game[0]} - {game[1]}₽" for game in games]) + f"\n\n💵 Итого: {total}₽"
    else:
        text = "🛒 Ваша корзина пуста"

    await callback.message.edit_text(
        text,
        reply_markup=get_cart_kb(user_id),
        parse_mode='HTML'
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("cart_game_"))
async def cart_game_selected(callback: types.CallbackQuery):
    game_id = int(callback.data.split("_")[2])
    cursor.execute("SELECT title, genre, price FROM games WHERE game_id = ?", (game_id,))
    game = cursor.fetchone()

    text = (
        f"🎮 <b>{game[0]}</b>\n\n"
        f"📝 Жанр: <i>{game[1]}</i>\n\n"
        f"💵 Цена: <b>{game[2]}₽</b>\n\n"
        f"🛒 Игра в вашей корзине"
    )

    await callback.message.edit_text(
        text,
        reply_markup=get_cart_game_kb(game_id)
    )
    await callback.answer()


@dp.callback_query(F.data == "clear_cart")
async def clear_cart(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    cursor.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
    conn.commit()

    await callback.message.edit_text(
        "🛒 Ваша корзина пуста",
        reply_markup=get_cart_kb(user_id)
    )
    await callback.answer("❌ Корзина очищена")


@dp.callback_query(F.data == "buy")
async def buy_games(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    cursor.execute('''
    SELECT g.game_id, g.title, g.price, g.login, g.password 
    FROM cart c 
    JOIN games g ON c.game_id = g.game_id 
    WHERE c.user_id = ?
    ''', (user_id,))
    games = cursor.fetchall()

    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    balance = cursor.fetchone()[0]

    total = sum(game[2] for game in games)

    if balance >= total:
        new_balance = balance - total
        cursor.execute("UPDATE users SET balance = ? WHERE user_id = ?", (new_balance, user_id))

        # for game in games:
        # cursor.execute("UPDATE games SET is_used = 1 WHERE game_id = ?", (game[0],))

        cursor.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
        conn.commit()

        games_list = "\n\n".join(
            [f"🎮 <b>{game[1]}</b>\n👤 Логин: <code>{game[3]}</code>\n🔑 Пароль: <code>{game[4]}</code>" for game in
             games])

        await callback.message.edit_text(
            f"✅ Покупка успешна!\n\n"
            f"Вы приобрели:\n\n{games_list}\n\n"
            f"💵 Сумма покупки: {total}₽\n"
            f"💰 Остаток на балансе: {new_balance}₽\n\n"
            f"<b>Сохраните эти данные!</b>",
            reply_markup=get_main_menu_kb(),
            parse_mode='HTML'
        )
    else:
        await callback.message.edit_text(
            f"❌ Недостаточно средств!\n\n"
            f"💵 Сумма покупки: {total}₽\n"
            f"💰 Ваш баланс: {balance}₽\n\n"
            f"Пополните баланс или удалите некоторые игры из корзины.",
            reply_markup=get_cart_kb(user_id)
        )
    await callback.answer()


@dp.callback_query(F.data == "balance")
async def show_balance(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    balance = cursor.fetchone()[0]

    await callback.message.edit_text(
        f"💰 Ваш баланс: {balance}₽",
        reply_markup=get_balance_kb()
    )
    await callback.answer()


@dp.callback_query(F.data == "add_balance")
async def add_balance(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "💳 Введите сумму для пополнения баланса (в рублях):",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="🔙 Назад", callback_data="balance")
        ]])
    )
    await state.set_state(AddBalanceState.amount)
    await callback.answer()


@dp.message(AddBalanceState.amount)
async def process_balance_amount(message: types.Message, state: FSMContext):
    try:
        amount = int(message.text)
        if amount <= 0:
            raise ValueError
    except ValueError:
        await message.answer("❌ Пожалуйста, введите корректную сумму (целое число больше 0):")
        return

    user_id = message.from_user.id
    cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
    conn.commit()

    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    new_balance = cursor.fetchone()[0]

    await message.answer(
        f"✅ Баланс успешно пополнен на {amount}₽\n"
        f"💰 Теперь ваш баланс: {new_balance}₽",
        reply_markup=get_main_menu_kb()
    )
    await state.clear()


@dp.message(Command("logs"))
async def send_logs(message: types.Message):
    if message.from_user.id not in ADMIN_USER_ID:
        logger.warning(f"User {message.from_user.id} tried to access logs")
        await message.answer("⛔ У вас нет прав для выполнения этой команды")
        return

    try:
        if not os.path.exists('bot.log') or os.path.getsize('bot.log') == 0:
            await message.answer("📭 Файл логов пуст или не существует")
            return

        log_file = FSInputFile('bot.log')
        await message.answer_document(
            document=log_file,
            caption=f"📋 Лог-файл бота\n🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

        with open('bot.log', 'w', encoding='utf-8') as f:
            f.write('')

        logger.info("Logs sent to admin and file cleared")
        await message.answer("✅ Логи успешно отправлены и файл очищен")

    except Exception as e:
        logger.error(f"Error sending logs: {e}")
        await message.answer(f"❌ Ошибка при отправке логов: {e}")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
