import random
import urllib.parse
import telebot
from telebot import types

# Токен вашего бота
bot = telebot.TeleBot("9174056572:AAEeBf1rTpbkHo1HnM2DNsTcSphIt9f6_84")

# Список команд для справки (без скрытых команд)
COMMANDS_INFO = """
🤖 Список доступных команд:
Используйте префикс **хаб** или **.** (например: `.курс`, `хаб цитата`):

• **курс** [кол-во] [валюта1] [валюта2] — конвертер валют
• **погода** [город] — узнать погоду
• **поиск** [запрос] — ссылки в поисковиках (синонимы: гугл, яндекс, найти)
• **монетка** — подбросить монетку (орёл/решка)
• **кубик** — бросить игральный кубик (1-6)
• **цитата** — одна из 50 случайных цитат
• **раскладка** [текст] — исправить раскладку (синоним: конв)
• **меню** — показать это сообщение и кнопки
"""

# Полный список из 50 цитат
QUOTES_LIST = [
    "«Единственный способ делать великую работу — любить то, что вы делаете.» — Стив Джобс",
    "«Будущее принадлежит тем, кто верит в красоту своей мечты.» — Элеонора Рузвельт",
    "«Лучшее время, чтобы посадить дерево, было 20 лет назад. Следующее лучшее время — сегодня.» — Китайская пословица",
    "«Не ждите. Время никогда не будет подходящим.» — Наполеон Хилл",
    "«То, что вы можете сделать или о чем мечтаете, начните делать.» — Иоганн Вольфганг фон Гете",
    "«Падайте семь раз и поднимайтесь восемь.» — Японская пословица",
    "«Сложнее всего начать действовать, все остальное зависит только от упорства.» — Амелия Эрхарт",
    "«Наш величайший успех не в том, чтобы никогда не падать, а в том, чтобы подниматься каждый раз.» — Конфуций",
    "«Кто хочет делать дело, находит средства; кто не хочет — находит причины.» — Сократ",
    "«Секрет успеха — двигаться вперед.» — Марк Твен",
    "«Жизнь — это то, что случается с вами, пока вы строите другие планы.» — Джон Леннон",
    "«Счастье не в том, чтобы делать всегда то, что хочешь, а в том, чтобы всегда хотеть того, что делаешь.» — Л.Н. Толстой",
    "«Жизнь измеряется не количеством вдохов, а моментами, когда от дыхания захватывает дух.» — Джордж Карлин",
    "«Мы становимся тем, о чем думаем.» — Эрнест Смит",
    "«Лучший способ предсказать будущее — создать его.» — Питер Друкер",
    "«Измените свои мысли, и вы измените свой мир.» — Норман Винсент Пил",
    "«Нельзя изменить направление ветра, но можно поднять паруса.» — Оскар Уайльд",
    "«Время — лучший учитель, но, к сожалению, оно убивает своих учеников.» — Бернард Шоу",
    "«Никогда не поздно стать тем, кем ты мог бы быть.» — Джордж Элиот",
    "«Жизнь — как вождение велосипеда. Чтобы сохранить равновесие, ты должен двигаться.» — Альберт Эйнштейн",
    "«Успех — это способность идти от неудачи к неудаче без потери энтузиазма.» — Уинстон Черчилль",
    "«Верьте, что можете, и полпути уже пройдено.» — Теодор Рузвельт",
    "«Действие — это главный ключ к успеху.» — Пабло Пикассо",
    "«Не бойтесь перемен. Чаще всего они происходят именно тогда, когда они необходимы.» — Дональд Трамп",
    "«Начинайте с того места, где вы находитесь. Используйте то, что у вас есть, и делайте все, что можете.» — Артур Эш",
    "«Сделайте первый шаг в вере. Вам не нужно видеть всю лестницу, просто сделайте первый шаг.» — Мартин Лютер Кинг",
    "«Вдохновение существует, но оно должно застать вас за работой.» — Пабло Пикассо",
    "«Сложнее всего победить самого себя.» — Цицерон",
    "«Смелость — это сопротивление страху, преодоление страха, а не его отсутствие.» — Марк Твен",
    "«Не бойся идти медленно, бойся стоять на месте.» — Китайская пословица",
    "«Каждый день может быть хорошим, но в каждом дне есть что-то хорошее.» — Аббат Фурро",
    "«Улыбка — это недорогой способ улучшить свою внешность.» — Шарль Горди",
    "«Если вы делаете то, что делали всегда, то получаете то, что получали всегда.» — Тони Роббинс",
    "«Удача любит подготовленный ум.» — Луи Пастер",
    "«Знания — это сокровище, которое всегда следует за тем, кто им владеет.» — Китайская пословица",
    "«Ничто так не открывает глаза на мир, как путешествия.» — Мигель де Сервантес",
    "«Каждая трудность, с которой вы сталкиваетесь, имеет тенденцию делать вас сильнее.» — Джоэл Остин",
    "«Великие умы обсуждают идеи. Средние умы обсуждают события. Мелкие умы обсуждают людей.» — Элеонора Рузвельт",
    "«Кто не делает ошибок, тот обычно не делает ничего.» — Иоганн Вольфганг фон Гете",
    "«Ваше время ограничено, не тратьте его, живя чужой жизнью.» — Стив Джобс",
    "«Самый сильный человек тот, у кого есть сила победить свои дурные привычки.» — Овидий",
    "«Радость не в вещах, она в нас самих.» — Рихард Вагнер",
    "«Живи так, будто умрешь завтра; учись так, будто будешь жить вечно.» — Махатма Ганди",
    "«Трудные времена рождают сильных людей.» — Восточная мудрость",
    "«Счастье — это когда тебя понимают, большое счастье — это когда тебя любят, настоящее счастье — это когда любишь ты.» — Конфуций",
    "«Успех — это 1% вдохновения и 99% потения.» — Томас Эдисон",
    "«Мудрость приходит с возрастом, но иногда возраст приходит один.» — Михаил Жванецкий",
    "«Величайшая слава в жизни заключается не в том, чтобы никогда не падать, а в том, чтобы подниматься каждый раз.» — Нельсон Мандела",
    "«Человек создан для счастья, как птица для полета.» — В.Г. Короленко",
    "«Настоящий успех измеряется не тем, чего вы достигли, а тем, какие препятствия вы преодолели на пути к этому.» — Букер Т. Вашингтон"
]

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    btn_kurs = types.InlineKeyboardButton("💱 Курс", callback_data="btn_kurs")
    btn_fun = types.InlineKeyboardButton("🎲 Играть", callback_data="btn_fun")
    btn_quote = types.InlineKeyboardButton("📜 Цитата", callback_data="btn_quote")
    btn_help = types.InlineKeyboardButton("📋 Список команд", callback_data="btn_help")
    
    markup.add(btn_kurs, btn_fun)
    markup.add(btn_quote, btn_help)
    
    bot.send_message(
        message.chat.id, 
        "Привет! Я бот-помощник.\n" + COMMANDS_INFO, 
        reply_markup=markup, 
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "btn_kurs":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "💱 Пример команды: `.курс 100 usd rub`", parse_mode="Markdown")
    elif call.data == "btn_fun":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "🎲 Попробуйте написать `.монетка` или `.кубик`", parse_mode="Markdown")
    elif call.data == "btn_quote":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, f"📜 *Цитата дня:*\n{random.choice(QUOTES_LIST)}", parse_mode="Markdown")
    elif call.data == "btn_help":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, COMMANDS_INFO, parse_mode="Markdown")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    raw_text = message.text.strip()
    text_lower = raw_text.lower()
    
    prefix = None
    command_text = ""
    
    if text_lower.startswith("хаб "):
        prefix = "хаб "
        command_text = text_lower[4:].strip()
    elif text_lower.startswith("."):
        prefix = "."
        command_text = text_lower[1:].strip()
        
    if prefix is None:
        return

    parts = command_text.split(maxsplit=1)
    cmd = parts[0] if parts else ""
    args = parts[1] if len(parts) > 1 else ""

    # Скрытая команда: привет
    if cmd == "привет":
        bot.send_message(message.chat.id, "Привет, чем могу помочь?")

    # Скрытая команда: как дела
    elif cmd in ["как дела?", "как дела"]:
        bot.send_message(message.chat.id, "Пока не родила")

    # 1. Погода
    elif cmd == "погода":
        if args:
            bot.send_message(message.chat.id, f"🌤 Погода в местности *{args}*: примерно +20°C, без осадков.", parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, "📍 Укажите город или село. Пример: `.погода Москва`", parse_mode="Markdown")

    # 2. Поиск
    elif cmd in ["поиск", "гугл", "яндекс", "найти", "найди", "искать"]:
        if args:
            encoded = urllib.parse.quote(args)
            google_url = f"https://www.google.com/search?q={encoded}"
            yandex_url = f"https://yandex.ru/search/?text={encoded}"
            text_resp = f"🔍 Результаты поиска для *{args}*:\n\n• [Google]({google_url})\n• [Яндекс]({yandex_url})"
            bot.send_message(message.chat.id, text_resp, parse_mode="Markdown", disable_web_page_preview=True)
        else:
            bot.send_message(message.chat.id, "🔍 Напишите, что искать. Пример: `.найти python`", parse_mode="Markdown")

    # 3. Монетка
    elif cmd in ["монетка", "орлрешка"]:
        result = random.choice(["Орел 🪙", "Решка 🪙"])
        bot.send_message(message.chat.id, f"Результат броска: *{result}*", parse_mode="Markdown")

    # 4. Кубик
    elif cmd in ["кубик", "кость"]:
        result = random.randint(1, 6)
        bot.send_message(message.chat.id, f"🎲 Вам выпало число: *{result}*", parse_mode="Markdown")

    # 5. Цитата
    elif cmd == "цитата":
        bot.send_message(message.chat.id, f"📜 *Цитата дня:*\n{random.choice(QUOTES_LIST)}", parse_mode="Markdown")

    # 6. Исправление раскладки
    elif cmd in ["раскладка", "конв"]:
        target_text = args
        if not target_text and message.reply_to_message and message.reply_to_message.text:
            target_text = message.reply_to_message.text
            
        if target_text:
            en_chars = "qwertyuiop[]asdfghjkl;'zxcvbnm,./QWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>?"
            ru_chars = "йцукенгшщзхъфывапролджэячсмитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,"
            trans_table = str.maketrans(en_chars + ru_chars, ru_chars + en_chars)
            fixed_text = target_text.translate(trans_table)
            bot.send_message(message.chat.id, f"🔤 Исправленный текст:\n{fixed_text}")
        else:
            bot.send_message(message.chat.id, "🔤 Укажите текст или ответьте командой `.раскладка` на сообщение.")

    # 7. Курс валют
    elif cmd in ["курс", "пары"]:
        clean_args = args.replace("/", " ").replace(" в ", " ").replace(" на ", " ")
        parts_args = clean_args.split()
        
        amount = 1.0
        base = "USD"
        quote = "RUB"
        
        try:
            if len(parts_args) >= 3:
                amount = float(parts_args[0])
                base = parts_args[1].upper()
                quote = parts_args[2].upper()
            elif len(parts_args) == 2:
                try:
                    amount = float(parts_args[0])
                    base = "USD"
                    quote = parts_args[1].upper()
                except ValueError:
                    base = parts_args[0].upper()
                    quote = parts_args[1].upper()
            elif len(parts_args) == 1 and parts_args[0]:
                base = parts_args[0].upper()
                quote = "RUB"
        except ValueError:
            pass

        rates = {"USD": 90.0, "EUR": 98.0, "USDT": 91.0, "BTC": 60000.0, "RUB": 1.0}
        
        if base in rates and quote in rates:
            in_rub = amount * rates[base] if base != "RUB" else amount
            result_val = in_rub / rates[quote] if quote != "RUB" else in_rub
            bot.send_message(message.chat.id, f"💱 {amount} {base} = *{result_val:.2f} {quote}*", parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, f"💱 Курс пары {base} / {quote}: (пример: 1 {base} = 90.0 {quote})")

    elif cmd in ["меню", "команды"]:
        send_welcome(message)
        
    else:
        bot.send_message(message.chat.id, f"❌ Неизвестная команда: `{cmd}`. Напишите `.меню` для справки.", parse_mode="Markdown")

bot.polling(none_stop=True)
