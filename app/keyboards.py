from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup

def games_keyboard(data_dict) -> InlineKeyboardMarkup:
    inline_buttons = [[] for _ in range(int(len(data_dict) / 4) + 1)]
    index = 0
    for game_name, game_id in data_dict.items():
        if len(inline_buttons[index]) == 4:
            index += 1
            inline_buttons[index].append(InlineKeyboardButton(text=game_name, callback_data=f'g{int(game_id)}'))
        else:
            inline_buttons[index].append(InlineKeyboardButton(text=game_name, callback_data=f'g{int(game_id)}'))
    back = []
    back.append(InlineKeyboardButton(text='🔙 Главное меню', callback_data='menu'))
    buttons = [*inline_buttons, back]
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return inline_keyboard


def friends_keyboard(data_dict) -> InlineKeyboardMarkup:
    inline_buttons = [[] for _ in range(int(len(data_dict) / 4) + 1)]
    index = 0
    for i in data_dict:
        if len(inline_buttons[index]) == 4:
            index += 1
            inline_buttons[index].append(InlineKeyboardButton(text=i['personaname'], callback_data=f'friend{i['steamid']}'))
        else:
            inline_buttons[index].append(InlineKeyboardButton(text=i['personaname'], callback_data=f'friend{i['steamid']}'))
    back = []
    back.append(InlineKeyboardButton(text='🔙 Главное меню', callback_data='menu'))
    buttons = [*inline_buttons, back]
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return inline_keyboard


def achievements_keyboard(achievement, app_id) -> InlineKeyboardMarkup:
    inline_buttons = [[] for _ in range(int(len(achievement) / 4) + 1)]
    index = 0
    for game in achievement:
        if len(inline_buttons[index]) == 4:
            index += 1
            inline_buttons[index].append(InlineKeyboardButton(text=game['name'], callback_data=f'{game['name']}+{app_id}'))
        else:
            inline_buttons[index].append(InlineKeyboardButton(text=game['name'], callback_data=f'{game['name']}+{app_id}'))
    back = []
    back.append(InlineKeyboardButton(text='🔙 Главное меню', callback_data='menu'))
    buttons = [*inline_buttons, back]
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return inline_keyboard


#------------------Создание клавиатуры для главной страницы----------------------
def main_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text="Статистика по CS2⚔️"),
            KeyboardButton(text="Достижения📋"),
            KeyboardButton(text="Друзья🫂"),
        ],
        [
            KeyboardButton(text="Профиль👤"),
            KeyboardButton(text="Привязать аккаунт"),
        ]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    return keyboard


def check_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text="Привязал"),

        ]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    return keyboard


def getout_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text="Главное меню"),

        ]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    return keyboard
