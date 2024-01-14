import telebot

import _db_helper_LFB
from config import FeedbackAboutBots_bot_TOKEN

bot = telebot.TeleBot(FeedbackAboutBots_bot_TOKEN)


@bot.message_handler(content_types=['document'])
def check_db(message):

    t = _db_helper_LFB.scan_directories(message.document.file_name)

    bot.delete_message(message.from_user.id, message.id)
    if t:
        bot.send_message(message.from_user.id, "Есть!")
    else:
        bot.send_message(message.from_user.id, "Нет!")


def test():
    import os

    def passage(file_name, folder):
        for element in os.scandir(folder):
            if element.is_file():
                if element.name == file_name:
                    yield folder
            else:
                yield from passage(file_name, element.path)

    t = passage('feedback_bot_v2.db', "C:\\Users\\User\\Documents\\GitHub")
    for i in t:
        print(i)


def test2(*args):
    print(*args)


if __name__ == '__main__':
    while True:
        command = input("Enter command: ")
        if command == "bot":
            bot.polling(skip_pending=True)
        elif command == "os":
            test()
        elif command == "args":
            test2(12, 12, 234, 234, 2342, 34, 2342, 3423, 4242)
        else:
            break
