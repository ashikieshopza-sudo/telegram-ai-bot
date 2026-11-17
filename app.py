import os
import telebot
import google.generativeai as genai

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TELEGRAM_TOKEN)

SYSTEM_PERSONA = (
    "তুমি একজন অত্যন্ত দক্ষ আইটি এক্সপার্ট এবং আমার পার্সোনাল লার্নিং মেন্টর। "
    "তুমি খুব সহজ ভাষায়, প্র্যাকটিক্যাল উদাহরণ দিয়ে আমাকে প্রোগ্রামিং, টেকনোলজি এবং আইটি প্রবলেম সলভিং শেখাবে।"
)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "হ্যালো! আমি আপনার পার্সোনাল আইটি মেন্টর এবং এআই কো-ওয়ার্কার। "
        "আজ থেকে আইটি এবং টেকনিক্যাল স্কিল বাড়ানোর যাত্রায় আমি আপনার সাথে আছি। "
        "বলুন, আজকে কোন টপিক বা প্রবলেম নিয়ে আমরা কাজ শুরু করব?"
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text
    try:
        prompt = f"{SYSTEM_PERSONA}\n\nUser Question: {user_text}"
        response = model.generate_content(prompt)
        reply_text = response.text
    except Exception as e:
        reply_text = "দুঃখিত, এই মুহূর্তে এআই ব্রেইন কানেক্ট করতে একটু সমস্যা হচ্ছে। আবার চেষ্টা করুন!"

    bot.reply_to(message, reply_text)

if __name__ == "__main__":
    print("AI Mentor Bot is running...")
    bot.infinity_polling()
