# MunSteam_tgbot

![Static Badge](https://img.shields.io/badge/%D0%9F%D0%BE%D1%81%D0%BC%D0%BE%D1%82%D1%80%D0%B5%D1%82%D1%8C_%D0%B4%D0%B5%D0%BC%D0%BE%D0%BD%D1%81%D1%82%D1%80%D0%B0%D1%86%D0%B8%D1%8E_%D1%82%D0%B5%D0%BB%D0%B5%D0%B3%D1%80%D0%B0%D0%BC_%D0%B1%D0%BE%D1%82%D0%B0-blue?link=https%3A%2F%2Ft.me%2Feasyoffer_bot)


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