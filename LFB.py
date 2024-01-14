import telebot
from telebot import types

from config import FeedbackAboutBots_bot_TOKEN
from about_LFB import about
from sql_LFB import DataBase, check_tables, get_record, print_data, get_info_about_message

bot = telebot.TeleBot(FeedbackAboutBots_bot_TOKEN)
current_stage = "None"
debug_stage = 0
is_finished = False

db_dict = {}


def manager(message):
    """
        This function determines which stage the user is currently at and what needs to be done at this stage.
        Returns True, if program has been finished, else False
    """
    global current_stage, debug_stage
    if message.text == "/start":
        check_tables()
    # recording necessary info about sent message
    get_info_about_message(message.from_user.id, message.text) if __name__ != "__main__" else ...
    if message.text == "/about":
        about(message, bot)
    elif message.text == "/admin" or debug_stage > 0 or debug_stage == -1:
        admin(message)
    elif current_stage == "None" and message.text == "/start":
        feedback(message)
    elif current_stage not in ["None", "Выбор", "Отзыв"]:
        bot.send_message(message.from_user.id, "<b>Извините, возникли неполадки в программе. "
                                               "Выполняю принудительное завершение работы...</b>",
                         parse_mode='html')
        bot.stop_bot()
        raise SystemError("Сбой в программе! Неправильное название этапа!")

    return is_finished


def admin(message):
    global debug_stage
    match debug_stage:
        case -1:
            bot.send_message(message.chat.id, "❌ Я вас не признаю")
            debug_stage = 0
        case 0:
            bot.send_message(message.chat.id, "👉 Ваше имя:")
            debug_stage += 1 if message.text == "Алексей" else -1
        case 1:
            bot.send_message(message.from_user.id, "👉 Ваше отношение к ЛГБТ, "
                             "БЛМ и движению неонацистов(неонацизм) в Украине одним словом:")
            debug_stage += 1 if message.text == "Говно" else -2
        case 2:
            bot.send_message(message.chat.id, "👉 Название Вашего YouTube-канала "
                                              "или Ваш любимый никнейм в играх:")
            debug_stage += 1 if message.text == "приколямба" else -3
        case 3:
            bot.send_message(message.chat.id, "👉 Ваш ID:")
            debug_stage += 1 if message.text == "1272372338" else -4
        case 4:
            bot.send_message(message.chat.id, "👉 Ваш пароль от аккаунта:")
            debug_stage += 1 if message.text == "пошёл нахуй уёбище ебучее" else -5
        case 5:
            bot.send_message(message.chat.id, "✔ Вы подтвердили, что являетесь разработчиком!")
            debug_stage += 2
        case 7:
            match message.text:
                case "/pr_d":
                    ...
                case "/check_db":
                    ...
                case "/add_db":
                    ...
                case "/ahelp":
                    ...
