import os
import telebot
from telebot import types
from flask import Flask
from threading import Thread

# 1. Сервер для UptimeRobot
app = Flask('')

@app.route('/')
def home():
    return "DogeTurbo Node is Live!"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True # Это предотвратит "зависание" потоков
    t.start()

# 2. Настройка бота
TOKEN = '8463306163:AAGkUpKohEXBkfqCE97iZlCRoy4DPnTjRQ8'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    # Возвращаем все три кнопки
    btn1 = types.InlineKeyboardButton("🚀 START MINTING", callback_data="mint")
    btn2 = types.InlineKeyboardButton("💰 WALLET", callback_data="wallet")
    btn3 = types.InlineKeyboardButton("❓ FAQ", callback_data="faq")
    markup.add(btn1, btn2, btn3)
    
    bot.send_message(
        message.chat.id, 
        "<b>DogeTurbo Terminal</b>\n\nStatus: 🟢 Connected\nNode: #8463\n\nChoose action:", 
        parse_mode="HTML", 
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "mint":
        bot.send_message(call.message.chat.id, "📝 Send Ticker name (e.g. DOGE):")
    elif call.data == "wallet":
        # ЗАМЕНИ YOUR_DOGE_ADDRESS НА СВОЙ РЕАЛЬНЫЙ АДРЕС НИЖЕ
        bot.send_message(call.message.chat.id, "<b>Your Deposit Address:</b>\n\n<code>YOUR_DOGE_ADDRESS</code>\n\n(Tap to copy)", parse_mode="HTML")
    elif call.data == "faq":
        bot.send_message(call.message.chat.id, "<b>How it works?</b>\n1. Deposit DOGE\n2. Enter Ticker\n3. Wait for mint confirmation.", parse_mode="HTML")

# 3. Запуск
if __name__ == "__main__":
    keep_alive()
    print("Бот перезапущен!")
    try:
        bot.remove_webhook()
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print(f"Ошибка: {e}")
