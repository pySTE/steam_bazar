import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = "7785027084:AAG7xbLlmuloH5DpYipjW8UZR8_Zq8gUhR8"  # Замените на токен вашего бота

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("group_id"))
async def get_group_id(message: types.Message):
    if message.chat.type in ["group", "supergroup"]:
        group_id = message.chat.id
        print(f"Group ID: {group_id}")
        await message.reply(f"ID этой группы: {group_id}")
    else:
        await message.reply("Эта команда работает только в группах!")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    print("Бот запущен... Ожидание команды /group_id в группе...")
    asyncio.run(main())
