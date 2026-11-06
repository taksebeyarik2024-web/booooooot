from datetime import datetime
import random
import urllib.parse
import telebot
from telebot import types

# Токен вашего бота
bot = telebot.TeleBot("9174056572:AAEeBf1rTpbkHo1HnM2DNsTcSphIt9f6_84")

# Хранилище языков для чатов (по умолчанию русский)
chat_languages = {}

# Словарь локализации (языки: ru, en, uk, de, kz)
LOCALES = {
    "ru": {
        "help": """
🤖 **Список доступных команд:**
Используйте префикс **хаб** или **.** (например: `.курс 5 доллар`, `хаб цит`, `.lang en`):
• **курс** [кол-во] [валюта] — мультиконвертер валют
• **погода** [город] — узнать погоду
• **поиск** [запрос] — ссылки в поисковиках
• **монетка** — подбросить монетку
• **кубик** — бросить игральный кубик
• **цит** — случайная цитата
• **переведи** [текст] — перевести текст
• **раскладка** [текст] — исправить раскладку (синоним: конв)
• **lang** [ru/en/uk/de/kz] — сменить язык бота
• **меню** — показать это сообщение
""",
        "welcome": "Привет! Я многоязычный бот-помощник.\n",
        "lang_changed": "✅ Язык успешно изменен на русский!",
        "weather": "🌤 Погода в местности",
        "coin_res": "Результат броска",
        "dice_res": "Вам выпало число",
        "quote_title": "📜 **Цитата дня:**",
        "translate_resp": "🔤 Перевод",
    },
    "en": {
        "help": """
🤖 **Available commands:**
Use prefix **hub** or **.** (e.g., `.курс 5 usd`, `hub цит`, `.lang ru`):
• **курс** [amount] [currency] — multi-currency converter
• **погода** [city] — get weather
• **поиск** [query] — search engine links
• **монетка** — flip a coin
• **кубик** — roll a dice
• **цит** — random quote
• **переведи** [text] — translate text
• **раскладка** [text] — fix keyboard layout (synonym: конв)
• **lang** [ru/en/uk/de/kz] — change bot language
• **меню** — show this message
""",
        "welcome": "Hello! I am your multilingual assistant bot.\n",
        "lang_changed": "✅ Language successfully changed to English!",
        "weather": "🌤 Weather in",
        "coin_res": "Coin flip result",
        "dice_res": "You rolled",
        "quote_title": "📜 **Quote of the day:**",
        "translate_resp": "🔤 Translation",
    },
    "uk": {
        "help": """
🤖 **Список доступних команд:**
Використовуйте префікс **хаб** або **.** (наприклад: `.курс 5 usd`, `хаб цит`):
• **курс** [кількість] [валюта] — мультиконвертер валют
• **погода** [місто] — дізнатися погоду
• **поиск** [запит] — посилання у пошукових системах
• **монетка** — підкинути монетку
• **кубик** — кинути гральний кубик
• **цит** — випадкова цитата
• **переведи** [текст] — перекласти текст
• **раскладка** [текст] — виправити розкладку (синонім: конв)
• **lang** [ru/en/uk/de/kz] — змінити мову бота
• **меню** — показати це повідомлення
""",
        "welcome": "Привіт! Я багатомовний бот-помічник.\n",
        "lang_changed": "✅ Мову успішно змінено на українську!",
        "weather": "🌤 Погода в місті",
        "coin_res": "Результат кидка",
        "dice_res": "Вам випало число",
        "quote_title": "📜 **Цитата дня:**",
        "translate_resp": "🔤 Переклад",
    },
    "de": {
        "help": """
🤖 **Verfügbare Befehle:**
Verwenden Sie das Präfix **hub** oder **.** (z. B. `.курс 5 usd`, `hub цит`):
• **курс** [Menge] [Währung] — Währungsrechner
• **погода** [Stadt] — Wetter abrufen
• **поиск** [Suche] — Suchmaschinen-Links
• **монетка** — Münzwurf
• **кубик** — Würfeln
• **цит** — Zitat des Tages
• **переведи** [Text] — Text übersetzen
• **раскладка** [Text] — Tastaturlayout korrigieren
• **lang** [ru/en/uk/de/kz] — Sprache ändern
• **меню** — Dieses Menü anzeigen
""",
        "welcome": "Hallo! Ich bin Ihr mehrsprachiger Assistent.\n",
        "lang_changed": "✅ Sprache erfolgreich auf Deutsch geändert!",
        "weather": "🌤 Wetter in",
        "coin_res": "Münzwurf-Ergebnis",
        "dice_res": "Gewürfelte Zahl",
        "quote_title": "📜 **Zitat des Tages:**",
        "translate_resp": "🔤 Übersetzung",
    },
    "kz": {
        "help": """
🤖 **Қолжетімді командалар:**
**хаб** немесе **.** префиксін қолданыңыз (мысалы: `.курс 5 usd`, `хаб цит`):
• **курс** [мөлшер] [валюта] — валюта конвертері
• **погода** [қала] — ауа райын білу
• **поиск** [сұрау] — іздеу жүйелерінің сілтемелері
• **монетка** — монета лақтыру
• **кубик** — сүйек лақтыру
• **цит** — кездейсоқ дәйексөз
• **переведи** [мәтін] — мәтінді аудару
• **раскладка** [мәтін] — пернетақта тілін түзету
• **lang** [ru/en/uk/de/kz] — тілді ауыстыру
• **меню** — көмек мәзірін көрсету
""",
        "welcome": "Сәлем! Мен сіздің көптілді көмекші ботыңызбын.\n",
        "lang_changed": "✅ Тіл сәтті қазақ тіліне өзгертілді!",
        "weather": "🌤 Қала бойынша ауа райы",
        "coin_res": "Монета нәтижесі",
        "dice_res": "Сізге түскен сан",
        "quote_title": "📜 **Күн дәйексөзі:**",
        "translate_resp": "🔤 Аударма",
    },
}


def get_locale(chat_id):
  lang = chat_languages.get(chat_id, "ru")
  return LOCALES.get(lang, LOCALES["ru"])


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
    "«Настоящий успех измеряется не тем, чего вы достигли, а тем, какие препятствия вы преодолели на пути к этому.» — Букер Т. Вашингтон",
]


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
  loc = get_locale(message.chat.id)
  markup = types.InlineKeyboardMarkup()
  btn_kurs = types.InlineKeyboardButton("💱 Курс", callback_data="btn_kurs")
  btn_fun = types.InlineKeyboardButton("🎲 Играть", callback_data="btn_fun")
  btn_quote = types.InlineKeyboardButton("📜 Цитата", callback_data="btn_quote")
  btn_help = types.InlineKeyboardButton("📋 Меню", callback_data="btn_help")

  markup.add(btn_kurs, btn_fun)
  markup.add(btn_quote, btn_help)

  bot.send_message(
      message.chat.id,
      loc["welcome"] + loc["help"],
      reply_markup=markup,
      parse_mode="Markdown",
  )


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
  loc = get_locale(call.message.chat.id)
  if call.data == "btn_kurs":
    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id,
        "💱 Пример команды: `.курс 5 доллар`",
        parse_mode="Markdown",
    )
  elif call.data == "btn_fun":
    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id,
        "🎲 Попробуйте написать `.монетка` или `.кубик`",
        parse_mode="Markdown",
    )
  elif call.data == "btn_quote":
    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id,
        f"{loc['quote_title']}\n{random.choice(QUOTES_LIST)}",
        parse_mode="Markdown",
    )
  elif call.data == "btn_help":
    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id, loc["help"], parse_mode="Markdown"
    )


@bot.message_handler(content_types=["text"])
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

  chat_id = message.chat.id
  loc = get_locale(chat_id)

  # Смена языка: .lang en / ru / uk / de / kz
  if cmd == "lang":
    if args in LOCALES:
      chat_languages[chat_id] = args
      new_loc = get_locale(chat_id)
      bot.send_message(chat_id, new_loc["lang_changed"])
    else:
      bot.send_message(
          chat_id,
          "🌐 Доступные языки / Available languages: `ru`, `en`, `uk`, `de`,"
          " `kz`\nПример: `.lang en`",
          parse_mode="Markdown",
      )
    return

  # Скрытая команда: привет
  if cmd == "привет":
    bot.send_message(chat_id, "Привет, чем могу помочь?")

  # Скрытая команда: как дела
  elif cmd in ["как дела?", "как дела"]:
    bot.send_message(chat_id, "Пока не родила")

  # Погода
  elif cmd == "погода":
    if args:
      bot.send_message(
          chat_id,
          f"🌤 {loc['weather']} *{args}*: примерно +20°C, без осадков.",
          parse_mode="Markdown",
      )
    else:
      bot.send_message(chat_id, "📍 Укажите город. Пример: `.погода Москва`")

  # Поиск
  elif cmd in ["поиск", "гугл", "яндекс", "найти", "найди", "искать"]:
    if args:
      encoded = urllib.parse.quote(args)
      google_url = f"https://www.google.com/search?q={encoded}"
      yandex_url = f"https://yandex.ru/search/?text={encoded}"
      text_resp = (
          f"🔍 Результаты поиска для *{args}*:\n\n•"
          f" [Google]({google_url})\n• [Яндекс]({yandex_url})"
      )
      bot.send_message(
          chat_id,
          text_resp,
          parse_mode="Markdown",
          disable_web_page_preview=True,
      )
    else:
      bot.send_message(chat_id, "🔍 Напишите, что искать. Пример: `.найти python`")

  # Переводчик: .переведи {текст}
  elif cmd == "переведи":
    if args:
      bot.send_message(
          chat_id,
          f"🔤 *Перевод:* {args} (эмулировано / обработано)",
          parse_mode="Markdown",
      )
    else:
      bot.send_message(
          chat_id, "🔤 Укажите текст для перевода. Пример: `.переведи Hello`"
      )

  # Монетка
  elif cmd in ["монетка", "орлрешка"]:
    result = random.choice(["Орел 🪙", "Решка 🪙"])
    bot.send_message(
        chat_id, f"{loc['coin_res']}: *{result}*", parse_mode="Markdown"
    )

  # Кубик
  elif cmd in ["кубик", "кость"]:
    result = random.randint(1, 6)
    bot.send_message(
        chat_id, f"{loc['dice_res']}: *{result}*", parse_mode="Markdown"
    )

  # Цитата (.цит)
  elif cmd == "цит":
    bot.send_message(
        chat_id,
        f"{loc['quote_title']}\n{random.choice(QUOTES_LIST)}",
        parse_mode="Markdown",
    )

  # Раскладка
  elif cmd in ["раскладка", "конв"]:
    target_text = args
    if (
        not target_text
        and message.reply_to_message
        and message.reply_to_message.text
    ):
      target_text = message.reply_to_message.text

    if target_text:
      en_chars = (
          "qwertyuiop[]asdfghjkl;'zxcvbnm,./QWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>?"
      )
      ru_chars = (
          "йцукенгшщзхъфывапролджэячсмитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,"
      )
      trans_table = str.maketrans(en_chars + ru_chars, ru_chars + en_chars)
      fixed_text = target_text.translate(trans_table)
      bot.send_message(chat_id, f"🔤 Исправленный текст:\n{fixed_text}")
    else:
      bot.send_message(chat_id, "🔤 Укажите текст или ответьте на сообщение.")

  # Курс валют
  elif cmd in ["курс", "пары"]:
    parts_args = args.split()
    amount = 5.0
    try:
      if parts_args:
        amount = float(parts_args[0])
    except ValueError:
      amount = 5.0

    eur = amount * 0.89726
    rub = amount * 81.99524
    uah = amount * 45.29700
    byn = amount * 2.99452
    kzt = amount * 450.12100
    gem = amount * 0.90910

    current_time = datetime.now().strftime("%d.%m.%Y %H:%M")

    response_text = (
        f"💹 {amount:g} Доллар США:\n\n"
        f"🇪🇺 {eur:.4f}\n"
        f"🇷🇺 {rub:.4f}\n"
        f"🇺🇦 {uah:.4f}\n"
        f"🇧🇾 {byn:.4f}\n"
        f"🇰🇿 {kzt:,.4f}".replace(",", " ")
        + f"\n💎 {gem:.4f}\n\n"
        f"⏱️ {current_time}"
    )

    bot.send_message(chat_id, response_text, parse_mode="Markdown")

  elif cmd in ["меню", "команды"]:
    send_welcome(message)


bot.polling(none_stop=True)
