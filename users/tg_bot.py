import logging
from telebot.async_telebot import AsyncTeleBot
from django.conf import settings
from .models import Profile
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async
import asyncio
import threading


bot = AsyncTeleBot(settings.API_TOKEN)

logging.basicConfig(level=logging.INFO)
logging.info('Бот запущен')

@bot.message_handler(commands=['start'])
async def process_start_command(message):
    try:
        activation_code = message.text.split(' ', 1)[1] if len(message.text.split(' ', 1)) > 1 else None
        if activation_code:
            profile = await sync_to_async(Profile.objects.get)(telegram_activation_code=activation_code)
            if profile:
                user = await sync_to_async(User.objects.get)(id=profile.user_id)
                if not user.is_active:
                    user.is_active = True
                    await sync_to_async(user.save)()
                    profile.telegram_username = message.from_user.username
                    await sync_to_async(profile.save)()

                    markup = InlineKeyboardMarkup()
                    markup.add(InlineKeyboardButton("Перейти на сайт", url='http://127.0.0.1:8000/'))
                    await bot.send_message(message.chat.id, "Аккаунт активирован", reply_markup=markup)
                else:
                    await bot.send_message(message.chat.id, "Аккаунт уже активирован")
            else:
                await bot.send_message(message.chat.id, "Неверная ссылка активации")
    except Exception as e:
        print("Error in process_start_command:", e)


def start_bot():
    asyncio.run(bot.polling())


if __name__ == "__main__":
    bot_thread = threading.Thread(target=start_bot, daemon=True)
    bot_thread.start()