import os
import telebot
from flask import Flask
from threading import Thread

TOKEN = os.environ.get("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive and running!"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "হ্যালো! আমি আপনার টেলিগ্রাম বট। সফলভাবে রেন্ডারে লাইভ হয়েছি!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text
    bot.reply_to(message, f"আপনার কথা পেয়েছি: {user_text}")

# ব্যাকগ্রাউন্ডে টেলিগ্রাম বট রান করার জন্য
def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    # ফ্লাস্ক সার্ভার চালু করা যাতে রেন্ডার পোর্ট পেয়ে যায়
    t = Thread(target=run_bot)
    t.start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
