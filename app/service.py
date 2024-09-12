import aiohttp
import asyncio
import locale
from datetime import datetime
from sqlalchemy.future import select

from app.keyboards import getout_keyboard, games_keyboard
from app.models import Session, UserMunSteam


async def fetch(message):
    url = 'https://munsteam.ru/user/api/telegram/'
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
    url = 'https://www.munsteam.ru/user/api/steam_info/'
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


async def get_stats_user(message, steam_id):
    url = 'https://www.munsteam.ru/statistic/api/user_statistic/'
    params = {'format': 'json', 'user_steam_id': steam_id}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                data_dict = {k: v for k, v in data[0].items()}
                stats_message = (
                    f"*Общее количество убийств*: {data_dict['total_kills']}\n"
                    f"*Общее количество смертей*: {data_dict['total_deaths']}\n"
                    f"*Время в игре*: {data_dict['time_played_hours']}\n"
                    f"*Закладка бомб*: {data_dict['total_planted_bombs']}\n"
                    f"*Разминирование бомб*: {data_dict['total_defused_bombs']}\n"
                    f"*Общий урон*: {data_dict['total_damage_done']}\n"
                    f"*Заработанные деньги*: {data_dict['money_earned']}\n"
                    f"*Победы в пистолетных раундах*: {data_dict['total_wins_pistolround']}\n"
                    f"*MVP*: {data_dict['total_mvps']}\n"
                    f"*Выигранные матчи*: {data_dict['total_matches_won']}\n"
                    f"*Сыгранные матчи*: {data_dict['total_matches_played']}\n"
                )
                if data:
                    await message.answer(stats_message, parse_mode='MarkdownV2')
                else:
                    await message.answer("Не получилось получить данные :(")
            else:
                await message.answer(f"Не удалось привязать аккаунт. Статус: {response.status}")


async def get_games_user(message, steam_id):
    url = 'https://www.munsteam.ru/achievements/api/achievements/gamesuser/'
    params = {'format': 'json', 'user_steam_id': steam_id}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                data_dict = {v: k for k, v in data[0]['games'].items()}
                if data:
                    await message.answer(f'Выберите игру по которой хотите получить достижения!', reply_markup=games_keyboard(data_dict))
                else:
                    await message.answer("Не получилось получить данные :(")
            else:
                await message.answer(f"Не удалось получить данные. Статус: {response.status}")