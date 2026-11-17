import os
import telebot
from flask import Flask
from threading import Thread
import google.generativeai as genai

# টোকেন ও এপিআই কি কনফিগারেশন
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# জেমিনি এআই সেটআপ
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel("gemini-1.5-flash")
else:
    gemini_model = None

bot = telebot.TeleBot(TELEGRAM_TOKEN, threaded=False)
app = Flask('')

@app.route('/')
def home():
    return "Gemini AI Mentor Bot is running!"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "হ্যালো! আমি আপনার জেমিনি এআই মেন্টর বট।\n\n"
        "যেকোনো প্রশ্ন করতে সরাসরি লিখুন অথবা কমান্ড ব্যবহার করুন:\n"
        "🔹 জেমিনির সাহায্য নিতে লিখুন: /gemini [আপনার প্রশ্ন]"
    )
    bot.reply_to(message, welcome_text)

# Gemini কমান্ড হ্যান্ডলার
@bot.message_handler(commands=['gemini'])
def ask_gemini(message):
    if not gemini_model:
        bot.reply_to(message, "দুঃখিত, জেমিনি এপিআই কি সেট করা নেই।")
        return
    
    prompt = message.text.replace("/gemini", "").strip()
    if not prompt:
        bot.reply_to(message, "দয়া করে /gemini কমান্ডের সাথে আপনার প্রশ্নটি লিখুন। যেমন: /gemini Python কী?")
        return
    
    try:
        response = gemini_model.generate_content(prompt)
        bot.reply_to(message, f"🤖 **Gemini AI:**\n\n{response.text}")
    except Exception as e:
        bot.reply_to(message, f"ত্রুটি ঘটেছে: {str(e)}")

# সাধারণ টেক্সট মেসেজের উত্তর দেওয়ার জন্য (ঐচ্ছিক)
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    if not gemini_model:
        bot.reply_to(message, "জেমিনি মডেল সেটআপ করা নেই।")
        return
    
    try:
        response = gemini_model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"ত্রুটি ঘটেছে: {str(e)}")

def run_bot():
    print("Starting Gemini bot polling...")
    bot.infinity_polling(skip_pending=True)

if __name__ == "__main__":
    t = Thread(target=run_bot)
    t.start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
