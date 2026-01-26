
import os
import telebot
from telebot import types
from flask import Flask
from threading import Thread

# 1. Мини-сервер для UptimeRobot
app = Flask('')

@app.route('/')
def home():
    return "Бот запущен!"

def run():
    # На Render порт всегда 10000 по умолчанию, если не задано иное
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 2. Настройка бота - ВСТАВЬ СВОЙ ТОКЕН НИЖЕ
# Просто замени текст ТВОЙ_ТОКЕН_ТУТ на токен от BotFather, оставь кавычки.
TOKEN = '8463306163:AAGkUpKohEXBkfqCE97iZlCRoy4DPnTjRQ8'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("🚀 START MINTING", callback_data="mint")
    btn2 = types.InlineKeyboardButton("💰 WALLET", callback_data="wallet")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "<b>DogeTurbo Terminal</b>\nStatus: Online", parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "mint":
        bot.send_message(call.message.chat.id, "Send Ticker name:")
    elif call.data == "wallet":
        bot.send_message(call.message.chat.id, "Address: <code>YOUR_DOGE_ADDRESS</code>", parse_mode="HTML")

# 3. Запуск
if __name__ == "__main__":
    keep_alive()
    print("Бот пошел в онлайн!")
    bot.infinity_polling()
