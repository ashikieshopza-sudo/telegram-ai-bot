import os
import telebot
from flask import Flask
from threading import Thread
import google.generativeai as genai
from openai import OpenAI

# টোকেন ও এপিআই কি কনফিগারেশন
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# জেমিনি ও ওপেনএআই সেটআপ
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel("gemini-1.5-flash")
else:
    gemini_model = None

openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

bot = telebot.TeleBot(TELEGRAM_TOKEN, threaded=False)
app = Flask('')

@app.route('/')
def home():
    return "AI Mentor Bot with Gemini & OpenAI is running!"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "হ্যালো! আমি আপনার এআই মেন্টর বট।\n\n"
        "ব্যবহার করার নিয়ম:\n"
        "🔹 জেমিনির সাহায্য নিতে লিখুন: /gemini [আপনার প্রশ্ন]\n"
        "🔹 চ্যাটজিপিটির সাহায্য নিতে লিখুন: /chatgpt [আপনার প্রশ্ন]"
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

# OpenAI (ChatGPT) কমান্ড হ্যান্ডলার
@bot.message_handler(commands=['chatgpt'])
def ask_openai(message):
    if not openai_client:
        bot.reply_to(message, "দুঃখিত, ওপেনএআই এপিআই কি সেট করা নেই।")
        return
    
    prompt = message.text.replace("/chatgpt", "").strip()
    if not prompt:
        bot.reply_to(message, "দয়া করে /chatgpt কমান্ডের সাথে আপনার প্রশ্নটি লিখুন। যেমন: /chatgpt What is Flask?")
        return
    
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        reply_text = response.choices[0].message.content
        bot.reply_to(message, f"🧠 **ChatGPT:**\n\n{reply_text}")
    except Exception as e:
        bot.reply_to(message, f"ত্রুটি ঘটেছে: {str(e)}")

def run_bot():
    print("Starting AI bot polling...")
    bot.infinity_polling(skip_pending=True)

if __name__ == "__main__":
    t = Thread(target=run_bot)
    t.start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
