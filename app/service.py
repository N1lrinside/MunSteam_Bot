import aiohttp
import asyncio
import locale
from datetime import datetime
from sqlalchemy.future import select

from app.keyboards import getout_keyboard
from app.models import Session, UserMunSteam


async def fetch(message):
    url = 'https://munsteam.ru/user/api/user/telegram/'
    params = {'format': 'json', 'telegram_id': message.from_user.id}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                if data:
                    data_dict = {k: v for i in data for k,v in i.items()}
                    steam_id = data_dict['steamid_user']
                    if steam_id is not None:
                        await message.answer("Аккаунт привязан", reply_markup=getout_keyboard())
                        await save_steam_id_to_db(message, steam_id)
                    else:
                        await message.answer("У вас не привязан стим аккаунт на сайте!", reply_markup=getout_keyboard())
                else:
                    await message.answer("Аккаунт не привязан")
            else:
                await message.answer(f"Не удалось привязать аккаунт. Статус: {response.status}")


async def get_profile_url(message, steam_id):
    url = 'https://www.munsteam.ru/user/api/user/steam_info/'
    params = {'format': 'json', 'steam_id': steam_id}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                data_dict = {k: v for k, v in data[0].items()}
                if data:
                    date_create_acc = datetime.fromisoformat(data_dict['createdacc_time'])
                    date_lastlogoff = datetime.fromisoformat(data_dict['lastlogoff_time'])
                    message_text = (
                        f"Ваш профиль, {message.from_user.full_name} 👤\n"
                        f"*Имя Steam:* [{data_dict['personaname']}]({data_dict['profileurl']})\n"
                        f"*Статус:* {data_dict['get_personastate_display']} \n"
                        f"*Профиль:* {data_dict['get_communityvisibilitystate_display']} 👤\n"
                        f"*Последний раз в сети:* {date_lastlogoff.strftime('%d %B %Y %H:%M')} \n"
                        f"*Дата создания аккаунта:* {date_create_acc.strftime('%d %B %Y %H:%M')} \n"
                    )

                    await message.answer_photo(data_dict['avatarfull'], caption=message_text, parse_mode='MarkdownV2')
                else:
                    await message.answer("Не получилось получить данные :(")
            else:
                await message.answer(f"Не удалось привязать аккаунт. Статус: {response.status}")


async def save_steam_id_to_db(message, steam_id):
    async with Session() as session:
        async with session.begin():
            stmt = select(UserMunSteam).filter_by(telegram_id=str(message.from_user.id))
            result = await session.execute(stmt)
            user = result.scalars().first()

            if user:
                user.steam_id = steam_id
                session.add(user)
                await session.commit()
            else:
                await message.answer("Пользователь не найден в базе данных.")
