import os
import telebot
from flask import Flask
from threading import Thread

TOKEN = os.environ.get("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "হ্যালো! আমি সফলভাবে রেন্ডারে লাইভ হয়েছি!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text
    bot.reply_to(message, f"আপনার কথা পেয়েছি: {user_text}")

def run_bot():
    bot.infinity_polling(skip_pending=True)

if __name__ == "__main__":
    t = Thread(target=run_bot)
    t.start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
