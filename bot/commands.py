# commands.py
from telegram import Update
from telegram.ext import CallbackContext


async def start(update: Update, context: CallbackContext):
    user_name = update.effective_user.first_name
    language_code = update.effective_user.language_code
    if language_code == "ru":
        start_message = (
            f"Привет, {user_name}!\n\n"
            "Это бот, созданный для преобразования видео в видеосообщения. "
            "Используйте команду /help для получения инструкций.\n\n"
            "Администратор: @username\n"  # Замените на ваше имя пользователя
            "Исходный код: [GitHub](https://github.com/7GitGuru/Telegram-Video-Bot)"
        )
    elif language_code == "uk":
        start_message = (
            f"Привіт, {user_name}!\n\n"
            "Це бот, призначений для перетворення відео в відеозаписи. "
            "Використовуйте команду /help для отримання інструкцій.\n\n"
            "Адміністратор: @username\n"  # Замініть на ваше ім'я користувача
            "Вихідний код: [GitHub](https://github.com/7GitGuru/Telegram-Video-Bot)"
        )
    else:
        # If language code is not Russian or Ukrainian, use English as default
        start_message = (
            f"Hello, {user_name}!\n\n"
            "This is a bot designed to convert videos into video messages. "
            "Use /help for instructions.\n\n"
            "Administrator: @username\n"  # Replace with your username
            "Source: [GitHub](https://github.com/7GitGuru/Telegram-Video-Bot)"
        )
    await update.message.reply_text(start_message, parse_mode="Markdown", disable_web_page_preview=True)


async def help(update: Update, context: CallbackContext):
    language_code = update.effective_user.language_code
    if language_code == "ru":
        help_message = (
            "<b>Как подготовить видео:</b>\n\n"
            "Есть три правила:\n"
            "1. Видео должно быть <b>квадратным</b>.\n"
            "2. Разрешение должно быть <b>360p</b>.\n"
            "3. Не длиннее <b>60 секунд</b>.\n\n"
            "Вы можете настроить эти параметры в меню прямо перед отправкой видео.\n\n"
            "<b>Что делать с видеосообщением после этого?</b>\n\n"
            "Вы можете переслать видеосообщение без тега 'переслано от'. Для этого выберите сообщение -> "
            "Переслать -> выберите получателя из списка -> "
            "в открывшемся диалоге внизу будет панель 'Переслать сообщение', нажмите на эту панель -> "
            "выберите 'Скрыть имя отправителя' -> "
            "Отправить сообщение."
        )
    elif language_code == "uk":
        help_message = (
            "<b>Як підготувати відео:</b>\n\n"
            "Є три правила:\n"
            "1. Відео повинно бути <b>квадратним</b>.\n"
            "2. Роздільна здатність повинна бути <b>360p</b>.\n"
            "3. Не довше <b>60 секунд</b>.\n\n"
            "Ви можете налаштувати ці параметри в меню прямо перед надсиланням відео.\n\n"
            "<b>Що робити з відеозаписом після цього?</b>\n\n"
            "Ви можете переслати відеоповідомлення без тегу 'переслано від'. Для цього виберіть повідомлення -> "
            "Переслати -> виберіть отримувача зі списку -> "
            "у відкритому діалозі внизу буде панель 'Переслати повідомлення', натисніть на цю панель -> "
            "виберіть 'Сховати ім'я відправника' -> "
            "Надіслати повідомлення."
        )
    else:
        # If language code is not Russian or Ukrainian, use English as default
        help_message = (
            "<b>How to Prepare a Video:</b>\n\n"
            "There are three rules:\n"
            "1. The video must be <b>square</b>.\n"
            "2. Resolution must be <b>360p</b>.\n"
            "3. Not longer than <b>60 seconds</b>.\n\n"
            "You can adjust these parameters in the menu just before sending the video.\n\n"
            "<b>What to do with the video message afterwards?</b>\n\n"
            "You can forward video message without the 'forwarded from' tag. To do this, select the  message -> "
            "Forward -> choose the recipient from the list -> "
            "in the opened dialog at the bottom, there will be a 'Forward message' panel, click on this panel -> "
            "select 'Hide sender's name' -> "
            "Send the message."
        )
    await update.message.reply_text(help_message, parse_mode="HTML")
