import telebot
from telebot import types

# Замените "9174056572:AAEeBf1rTpbkHo1HnM2DNsTcSphIt9f6_84" на токен вашего бота от @BotFather
bot = telebot.TeleBot("9174056572:AAEeBf1rTpbkHo1HnM2DNsTcSphIt9f6_84")

# Список команд для справки
COMMANDS_INFO = """
🤖 Список доступных команд:
Используйте префикс хаб или . (например: .курс или хаб курс):

• курс — узнать курс валют
• вики — поиск по Википедии
• привет — поздороваться с ботом
• как дела? — узнать как дела
• меню — показать это сообщение и кнопки
"""

# Команда /start (показывает приветствие и кнопки)
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    btn_kurs = types.InlineKeyboardButton("💱 Курс", callback_data="btn_kurs")
    btn_wiki = types.InlineKeyboardButton("📚 Вики", callback_data="btn_wiki")
    btn_help = types.InlineKeyboardButton("📋 Список команд", callback_data="btn_help")
    
    markup.add(btn_kurs, btn_wiki)
    markup.add(btn_help)
    
    bot.send_message(
        message.chat.id, 
        "Привет! Я бот с поддержкой команд через префиксы хаб и .\n" + COMMANDS_INFO, 
        reply_markup=markup, 
        parse_mode="Markdown"
    )

# Обработка нажатий на инлайн-кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "btn_kurs":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "💱 Актуальный курс: 1 USD = (ваш курс здесь)")
    elif call.data == "btn_wiki":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "📚 Чтобы найти в вики, напишите: .вики ваш_запрос", parse_mode="Markdown")
    elif call.data == "btn_help":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, COMMANDS_INFO, parse_mode="Markdown")

# Обработка текстовых сообщений с префиксами "хаб" и "."
@bot.message_handler(content_types=['text'])
def handle_text(message):
    raw_text = message.text.strip()
    text_lower = raw_text.lower()
    
    prefix = None
    command_text = ""
    
    # Проверяем префиксы
    if text_lower.startswith("хаб "):
        prefix = "хаб "
        command_text = text_lower[4:].strip()
    elif text_lower.startswith("."):
        prefix = "."
        command_text = text_lower[1:].strip()
        
    # Если сообщение без префикса — игнорируем его
    if prefix is None:
        return

    # 1. .курс / хаб курс
    if command_text == "курс":
        bot.send_message(message.chat.id, "💱 Текущий курс валют: 1 USD = 90 RUB (пример)")
        
    # 2. .вики / хаб вики
    elif command_text.startswith("вики"):
        query = command_text[4:].strip()
        if query:
            bot.send_message(message.chat.id, f"📚 Результаты поиска по запросу *{query}*: (тут будет статья)", parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, "📚 Укажите, что именно искать. Например: .вики python", parse_mode="Markdown")
            
    # 3. .привет / хаб привет
    elif command_text == "привет":
        bot.send_message(message.chat.id, "Привет, чем могу помочь?")
        
    # 4. .как дела? / хаб как дела? (также обрабатываем без знака вопроса на всякий случай)
    elif command_text in ["как дела?", "как дела"]:
        bot.send_message(message.chat.id, "Пока не родила")
        
    # Команда меню через текст
    elif command_text in ["меню", "команды"]:
        send_welcome(message)
        
    else:
        bot.send_message(message.chat.id, f"❌ Неизвестная команда: {command_text}. Напишите .меню для справки.", parse_mode="Markdown")

# Запуск бота
bot.polling(none_stop=True)
