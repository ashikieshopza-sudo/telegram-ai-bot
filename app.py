import os
import telebot

TOKEN = os.environ.get("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "হ্যালো! আমি আপনার টেলিগ্রাম বট। সফলভাবে রেন্ডারে লাইভ হয়েছি!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text
    bot.reply_to(message, f"আপনার কথা পেয়েছি: {user_text}")

if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()
