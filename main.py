import os
import telebot
from telebot import types
from flask import Flask
from threading import Thread

# 1. Создаем мини-сайт для UptimeRobot
app = Flask('')

@app.route('/')
def home():
    return "Бот DogeTurbo запущен!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 2. Настраиваем самого бота
# Берем токен из секретов (Environment Variables на Render)
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_mint = types.InlineKeyboardButton("🚀 START MINTING", callback_data="mint")
    btn_wallet = types.InlineKeyboardButton("💰 WALLET", callback_data="wallet")
    markup.add(btn_mint, btn_wallet)
    
    bot.send_message(
        message.chat.id, 
        "<b>DogeTurbo Terminal</b>\nStatus: Connected", 
        parse_mode="HTML", 
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "mint":
        bot.send_message(call.message.chat.id, "Send Ticker name:")
    elif call.data == "wallet":
        bot.send_message(call.message.chat.id, "Your Address: <code>YOUR_DOGE_ADDRESS</code>", parse_mode="HTML")

# 3. Запуск
if __name__ == "__main__":
    keep_alive()  # Запускает сайт на фоне
    print("Бот пошел в онлайн!")
    bot.infinity_polling
  ()
