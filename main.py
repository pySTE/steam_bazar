import logging
import sqlite3

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token="6899662778:AAFKyYTqDUTfnvbVjmqowxqy_pDjFLFGk60")
dp = Dispatcher()

conn = sqlite3.connect('steam_shop.db')
cursor = conn.cursor()


def create_tables():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        balance INTEGER DEFAULT 0
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
    conn.commit()


create_tables()


def populate_games_data():
    cursor.execute("SELECT COUNT(*) FROM games")
    count = cursor.fetchone()[0]

    if count == 0:
        games_data = [
            ("Prototype 2", "Action", "rwgran1", "wet444wed", 299),
            ("Alan Wake", "Horror", "rwgran1", "wet444wed", 199),
            ("Paint the Town Red", "Action", "rzm745", "Rzm85770923", 149),
            ("Grand Theft Auto IV: The Complete Edition", "Action", "rzm745", "Rzm85770923", 249),
            ("Tropico 6", "Strategy", "liyagarcueva97", "CxvMhK9dPkUaIb", 299),
            ("GTA VICE CITY", "Action", "alp21cm", "10306969970aA", 99),
            ("ELDEN RING", "RPG", "Thragg_767", "ev8Z5YyvY42RmiX", 299),
            ("Resident Evil 4 Remake", "Horror", "bejdw24074", "https://steamkk.com", 299),
            ("Far cry 3", "Action", "youallsuck_911", "Adje2003a.1", 199),
            ("BLACK MYTH: WUKONG DELUX", "Action", "mario_wukong", "QCP7PFHMW4VV", 299),
            ("Cyberpunk 2077", "RPG", "icpropenin1988", "siski33Fh845X3BYiBLZyb1987", 299),
            ("Resident Evil Village", "Horror", "nikintolya92", "aJMpnB9GtONAyY1Q", 249),
            ("Far Cry 5", "Action", "dr4xon22", "ZIa_B--Z", 249),
            ("Assassin's Creed Chronicles India", "Adventure", "kxzoi70142", "VkY5EauB", 149),
            ("Assassin's Creed Chronicles China", "Adventure", "kxzoi70142", "VkY5EauB", 149),
            ("Assassin's Creed Chronicles Russia", "Adventure", "kxzoi70142", "VkY5EauB", 149),
            ("Assassin's Creed Brotherhood", "Action", "kxzoi70142", "VkY5EauB", 199),
            ("Mortal Combat X", "Fighting", "leo3d3", "tricolor231002", 199),
            ("Lords of the Fallen Deluxe Edition", "RPG", "rkwoh77645", "uofh08187V", 249),
            ("Call Of Duty WW2", "Shooter", "brbba2063", "che600220", 249),
            ("Dead Cells", "Roguelike", "hsrp18939", "3HjumZTz334I", 149),
            ("Five Nights at Freddy's Security Breach", "Horror", "nojevik__0", "wwe123456", 199),
            ("Borderlands 3", "Shooter", "ivy_wreathh", "yT1ML3YWe3dw52x", 299),
            ("Fallout 4", "RPG", "swfushe4", "Sw654247", 249),
            ("GTA 4", "Action", "wqm322495", "ac7QPfa3", 199),
            ("Assassin's creed 3 Remastered", "Action", "junjun888666733", "Xiaohejiaoao78965", 249),
            ("Resident Evil 7 Biohazard", "Horror", "jocuriargenrinia", "70Games.net92", 199),
            ("cuphead", "Platformer", "su0wn1hf", "UOipTT58vG5XZ1", 149),
            ("LITTLE NIGHTMARES", "Horror", "DecorousThoughtlessWhale", "Weirdmice91", 99),
            ("maneater", "Action", "yrij69325", "xmp8eADW", 199),
            ("Alien Isolation", "Horror", "jiaoaohehe188940", "junyi1139908", 149),
            ("tomb raider", "Adventure", "KickeyGame33", "I81PJDWCAS341FA", 149),
            ("kingdom Come: deliverance II", "RPG", "phvmg47604", "bfmjj99570", 299),
            ("Call of Duty: Modern Warfare 2 (2009)", "Shooter", "dimkoxd", "Dimko1995", 199),
            ("Terraria", "Sandbox", "charizardkingg", "Ronnie-13", 99),
            ("Slime Rancher", "Simulation", "charizardkingg", "Ronnie-13", 149),
            ("Age of Empires III: Definitive Edition", "Strategy", "komski01", "omarca06", 199),
            ("Watch Dogs Legion", "Action", "Bt5Pd3Zm9Sz4", "Yk2Ho8Wl5Im2", 299),
            ("hollow knight", "Metroidvania", "niodev", "funpay.onibist.users.5871937", 149),
            ("Need For Speed Heat", "Racing", "rd5977", "951753852.ACHU", 249),
            ("hotline miami", "Action", "keraoff", "v,!86QZSG(<e6:<", 99),
            ("Stray", "Adventure", "wbtq1088322", "steamok4566H", 199),
            ("Prototype", "Action", "axelturba3660", "monster3660", 149),
            ("HEARTS OF IRON IV", "Strategy", "meteprotr", "3D88ASX2AMCG", 199),
            ("Mortal Kombat 11", "Fighting", "kintygabobs1981", "XIdg5JiQZ11978", 249),
            ("Warhammer 40,000: Space Marine 2", "Action", "willianphillips7u", "mwe8p9SO4y1998", 299),
            ("EA SPORTS FC 25", "Sports", "neifreebzapme1973", "2y6rS0eJ6v2000", 299),
            ("Metro exodus", "Shooter", "chriswest6k", "xgfb9z5s", 249),
            ("Metro last light redux", "Shooter", "chriswest6k", "xgfb9z5s", 149),
            ("metro 2033 redux", "Shooter", "chriswest6k", "xgfb9z5s", 149),
            ("resident evil 2", "Horror", "lthNoviokv1", "hxrTV21zqgpkRuAnTAY0", 249),
            ("frostpunk 2", "Strategy", "lkzra09777", "siski33FpndvDpZ066475", 299),
            ("Dead Island 2", "Action", "cbkse74345", "siski33BYkJWT6HiZM7lhirtXsk", 299),
            ("God of war", "Action", "jmyhtrPtaosv1", "siski33hkFpEiHgWvccQV", 299),
            ("spider man remastered", "Action", "josephlighting98", "STEAM_ACCOUNT_64DVFndjei397421", 299),
            ("the last of us part 1", "Adventure", "tijodeme1978", "v0329fETm71987", 299)
        ]

        cursor.executemany(
            "INSERT INTO games (title, genre, login, password, price) VALUES (?, ?, ?, ?, ?)",
            games_data
        )
        conn.commit()


populate_games_data()


class AddBalanceState(StatesGroup):
    amount = State()


def get_main_menu_kb():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="🕹️ Каталог игр", callback_data="catalog"),
        InlineKeyboardButton(text="🛒 Корзина", callback_data="cart"),
        InlineKeyboardButton(text="💰 Баланс", callback_data="balance"),
        InlineKeyboardButton(text="💳 Пополнить баланс", callback_data="add_balance")
    )
    builder.adjust(2)
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


def get_game_details_kb(game_id, in_cart=False):
    builder = InlineKeyboardBuilder()
    if not in_cart:
        builder.add(InlineKeyboardButton(text="🛒 Добавить в корзину", callback_data=f"add_to_cart_{game_id}"))
    else:
        builder.add(InlineKeyboardButton(text="❌ Удалить из корзины", callback_data=f"remove_from_cart_{game_id}"))
    builder.add(InlineKeyboardButton(text="🔙 Назад",
                                     callback_data=f"genre_{cursor.execute('SELECT genre FROM games WHERE game_id = ?', (game_id,)).fetchone()[0]}"))
    builder.adjust(1)
    return builder.as_markup()


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

    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()

    await message.answer(
        "🎮 Добро пожаловать в магазин Steam игр!\n\n"
        "Здесь вы можете купить игры для Steam по выгодным ценам.",
        reply_markup=get_main_menu_kb()
    )


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

    await callback.message.edit_text(
        text,
        reply_markup=get_game_details_kb(game_id, in_cart),
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

        for game in games:
            cursor.execute("UPDATE games SET is_used = 1 WHERE game_id = ?", (game[0],))

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


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
