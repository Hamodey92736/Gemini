import google.generativeai as genai
import telebot
import datetime
from telebot import types

# Set up Google Generative AI
genai.configure(api_key="AIzaSyBtv6W1BL7GrcQD14P07nKdG50vHucNouU")

# Define the model generation configuration
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

# Define the safety settings for the model
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

# Create the Generative Model instance
model = genai.GenerativeModel(model_name="gemini-1.0-pro-latest",
               generation_config=generation_config,
               safety_settings=safety_settings)

# Set up Telegram bot
token = "7218686976:AAF9sDAr5tz8Nt_eMBoOl9-2RR6QsH5onTo"
bot = telebot.TeleBot(token)

# Handle '/start' command to send a welcome message
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    subscribe_button = types.InlineKeyboardButton("𝗦𝗰𝗼𝗿𝗽𝗶𝗼𝗻 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 ✍🏻", url="https://t.me/Scorpion_scorp")
    markup.add(subscribe_button)

    bot.send_message(
        message.chat.id,
        "<a href='https://t.me/ScorGPTbot'>𝗦𝗰𝗼𝗿𝗽𝗶𝗼𝗻 𝗚𝗣𝗧 𝟰</a>\n\n<b>✎┊‌ أهلاً بك في بوت الذكاء الاصطناعي الخاص بسورس العقرب. يمكنك طرح أي سؤال أو طلب، وسنكون سعداء بالإجابة عليه إن شاء الله 😁</b>\n\nالمطور <a href='https://t.me/Zo_r0'>𝗠𝗼𝗵𝗮𝗺𝗲𝗱</a> \nالمطور <a href='https://t.me/I_e_e_l'>𝗔𝗹𝗹𝗼𝘂𝘀𝗵</a>",
        parse_mode='HTML',
        disable_web_page_preview=True,
        reply_markup=markup
    )

# Handle messages from users
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    user_message = message.text
    message_id = bot.send_message(message.chat.id, "*✎┊‌ 𝗪𝗮𝗶𝘁 𝗺𝗲 ⏳*", parse_mode='Markdown').message_id

    try:
        # Generate a response using the model
        prompt_parts = [user_message]
        response = model.generate_text(prompt_parts)

        final_response = f"*العقرب:*\n{response['candidates'][0]['output']}"

        if any(phrase in user_message for phrase in ["من صنعك", "من هو صاحبك", "من أنشأك", "من انت", "من مطورك", "من مبرمج البوت", "من مبرمجك", "من مطور البوت"]):
            bot.send_message(message.chat.id, "*العقرب:*\n\n*أنا نموذج ذكاء اصطناعي تمت برمجتي بواسطة فريق العقرب *", parse_mode='Markdown')

        elif any(phrase in user_message for phrase in ["الوقت", "التاريخ"]):
            now = datetime.datetime.now()
            time = now.strftime("%H:%M")
            date = now.strftime("%Y-%m-%d")
            bot.send_message(message.chat.id, f"*العقرب:*\n\n*الوقت المحلي:* {time} _بتوقيت الرياض / السعودية_\n*التاريخ المحلي:* {date}", parse_mode='Markdown')

        elif any(phrase in user_message for phrase in ["كيف حالك", "كيف انت"]):
            bot.send_message(message.chat.id, "*العقرب:*\n*انا بخير والحمد لله وانت كيف حالك .*", parse_mode='Markdown')

        elif any(phrase in user_message for phrase in ["سورس العقرب", "العقرب"]):
            bot.send_message(message.chat.id, "*العقرب:*\n*اقوى سورس تلغرام عربي.*", parse_mode='Markdown')

        else:
            bot.send_message(message.chat.id, final_response, parse_mode='Markdown')

        bot.delete_message(message.chat.id, message_id)

    except Exception as e:
        bot.send_message(message.chat.id, "*العقرب:*\n\n*عذراً، لا يمكنني الإجابة على سؤالك.*", parse_mode='Markdown')
        bot.delete_message(message.chat.id, message_id)

# Start the bot
bot.polling()
