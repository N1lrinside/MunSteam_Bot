from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from sqlalchemy.future import select

from app.service import fetch, get_profile_url, get_stats_user, get_games_user, get_achievements_game, get_description_game, get_friends_user, get_friends_info
from app.keyboards import main_keyboard, check_keyboard
from app.models import Session, UserMunSteam

router = Router()


#------------------Начало работы бота с команды /start----------------------
@router.message(lambda call: call.text=='/start' or call.text=='Главное меню')
async def command_start(message: Message) -> None:
    async with Session() as session:
        async with session.begin():
            # Проверяем, существует ли пользователь
            stmt = select(UserMunSteam).filter_by(telegram_id=str(message.from_user.id))
            result = await session.execute(stmt)
            user = result.scalars().first()

            # Если пользователь не существует, создаем его
            if not user:
                user = UserMunSteam(telegram_id=str(message.from_user.id))
                session.add(user)
                await session.commit()  # Сохраняем изменения

    await message.answer(f"Привет! Я бот, который собирает твои данные с сайта munsteam.ru ",
                         reply_markup=main_keyboard())


#------------------Выбор фильма/сериала----------------------
@router.message(F.text == 'Привязать аккаунт')
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Перейди по ссылке и войдите в свой аккаунт https://munsteam.ru/user/profile/?telegram_id={message.from_user.id}", reply_markup=check_keyboard())


@router.message(F.text == 'Привязал')
async def command_start_handler(message: Message) -> None:
    await fetch(message)


#------------------Профиль пользователя со статистикой----------------------
@router.message(F.text == 'Профиль👤')
async def get_profile_user(message: Message):
    async with Session() as session:
        async with session.begin():
            stmt = select(UserMunSteam).filter_by(telegram_id=str(message.from_user.id))
            result = await session.execute(stmt)
            user = result.scalars().first()
            if user.steam_id is not None:
                await get_profile_url(message, user.steam_id)
            else:
                await message.answer(f"Ваш профиль, {message.from_user.full_name} 👤\n")


@router.message(F.text == 'Статистика по CS2⚔️')
async def get_profile_user(message: Message):
    async with Session() as session:
        async with session.begin():
            stmt = select(UserMunSteam).filter_by(telegram_id=str(message.from_user.id))
            result = await session.execute(stmt)
            user = result.scalars().first()
            if user.steam_id is not None:
                await get_stats_user(message, user.steam_id)
            else:
                await message.answer(f"У вас не привязан аккаунт")
                await message.answer(
                    f"Перейди по ссылке и войдите в свой аккаунт https://munsteam.ru/user/profile/?telegram_id={message.from_user.id}",
                    reply_markup=check_keyboard())


@router.message(F.text == 'Достижения📋')
async def get_profile_user(message: Message):
    async with Session() as session:
        async with session.begin():
            stmt = select(UserMunSteam).filter_by(telegram_id=str(message.from_user.id))
            result = await session.execute(stmt)
            user = result.scalars().first()
            if user.steam_id is not None:
                await get_games_user(message, user.steam_id)
            else:
                await message.answer(f"У вас не привязан аккаунт")
                await message.answer(
                    f"Перейди по ссылке и войдите в свой аккаунт https://munsteam.ru/user/profile/?telegram_id={message.from_user.id}",
                    reply_markup=check_keyboard())


@router.callback_query(lambda call: call.data[0] == 'g')
async def get_achievements_games(callback: CallbackQuery):
    async with Session() as session:
        async with session.begin():
            stmt = select(UserMunSteam).filter_by(telegram_id=str(callback.from_user.id))
            result = await session.execute(stmt)
            user = result.scalars().first()
            if user.steam_id is not None:
                await get_achievements_game(callback, user.steam_id, callback.data[1:])
            else:
                await callback.message.answer(f"У вас не привязан аккаунт")
                await callback.message.answer(
                    f"Перейди по ссылке и войдите в свой аккаунт https://munsteam.ru/user/profile/?telegram_id={callback.from_user.id}",
                    reply_markup=check_keyboard())


@router.callback_query(lambda call: '+' in call.data)
async def get_description_achievement(callback: CallbackQuery):
    async with Session() as session:
        async with session.begin():
            stmt = select(UserMunSteam).filter_by(telegram_id=str(callback.from_user.id))
            result = await session.execute(stmt)
            user = result.scalars().first()
            index_plus = callback.data.index('+')
            if user.steam_id is not None:
                await get_description_game(callback, user.steam_id, callback.data[index_plus + 1:], callback.data[:index_plus])
            else:
                await callback.message.answer(f"У вас не привязан аккаунт")
                await callback.message.answer(
                    f"Перейди по ссылке и войдите в свой аккаунт https://munsteam.ru/user/profile/?telegram_id={callback.from_user.id}",
                    reply_markup=check_keyboard())


@router.callback_query(F.data == 'menu')
async def going_to_menu(callback: CallbackQuery):
    await command_start(callback.message)


@router.message(F.text == 'Друзья🫂')
async def get_profile_user(message: Message):
    async with Session() as session:
        async with session.begin():
            stmt = select(UserMunSteam).filter_by(telegram_id=str(message.from_user.id))
            result = await session.execute(stmt)
            user = result.scalars().first()
            if user.steam_id is not None:
                await get_friends_user(message, user.steam_id)
            else:
                await message.answer(f"У вас не привязан аккаунт")
                await message.answer(
                    f"Перейди по ссылке и войдите в свой аккаунт https://munsteam.ru/user/profile/?telegram_id={message.from_user.id}",
                    reply_markup=check_keyboard())


@router.callback_query(lambda call: call.data[0:6] == 'friend')
async def get_achievements_games(callback: CallbackQuery):
    async with Session() as session:
        async with session.begin():
            stmt = select(UserMunSteam).filter_by(telegram_id=str(callback.from_user.id))
            result = await session.execute(stmt)
            user = result.scalars().first()
            if user.steam_id is not None:
                await get_friends_info(callback, user.steam_id)
            else:
                await callback.message.answer(f"У вас не привязан аккаунт")
                await callback.message.answer(
                    f"Перейди по ссылке и войдите в свой аккаунт https://munsteam.ru/user/profile/?telegram_id={callback.from_user.id}",
                    reply_markup=check_keyboard())

