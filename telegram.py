import telebot
import const
# import dao

bot = telebot.TeleBot(const.TELEGRAM_TOKEN)

# def save_chat_id(chat_id, username):
#     dao.updateChatIdForUser(chat_id, username)
#     pass


# @bot.message_handler(commands=['start'])
# def send_welcome(message):
#     chatId = message.from_user.id
#     userName = message.from_user.username
#     save_chat_id(chatId, userName)
#     bot.send_message(chat_id=chatId, text="Registered success !");


def sendMessage(msg, chatId):
    try:
        print(msg)
        bot.send_message(chat_id=chatId, text=msg,disable_web_page_preview=True,parse_mode="html")
    except Exception as e:
        print("Error telegram id " + str(chatId))


def start():
    bot.polling()
