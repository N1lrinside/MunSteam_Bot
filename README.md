# MunSteam_tgbot

**MunSteam_tgbot** – telegram бот, который собирает данные пользователя, благодаря api munsteam.ru

## Установка

Склонируйте репозиторий
```
git clone https://github.com/N1lrinside/MunSteam_Bot
```
Перейдите в папку с проектом
```
cd MunSteam_Bot
```
Создайте и запустите виртуальное окружение
```
python -m venv venv
source venv/bin/activate
```
Загрузите зависимости
```
pip install -r requirements.txt
```
Или так
```
poetry install
```
Создайте своего телеграм бота через BotFather и получите токен

Создайте в папке проекта файл .env и пропишите в нем токен

Не забудьте добавить телеграм бота в качестве админа в свои каналы (они обязательно должны быть публичными)

Запустите бота
```
python main.py
```
