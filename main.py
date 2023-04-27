import telebot
import threading
import time

from parse_urk_pravda import get_all_news, get_new_news

bot = telebot.TeleBot("5996577299:AAG5toKk9eNcUi6DA3tXRbX5yUqPEiZQps4", parse_mode="MARKDOWN")


def get_user_ids():
    with open("user_ids", 'r') as f:
        return set([int(line.strip()) for line in f])


def add_user_id(user_id):
    if user_id not in get_user_ids():
        print("One more new user. Id is", user_id)
        with open("user_ids", 'a') as f:
            f.write('\n' + str(user_id))


@bot.message_handler(commands=['start'])
def send_welcome(message):
    add_user_id(message.from_user.id)
    bot.send_message(message.from_user.id,
                     "Я повідомлю, щойно новина зявиться на сайті https://www.pravda.com.ua/news/")


def polling_function():
    print("start polling_function")
    new_news = get_new_news()
    user_ids = get_user_ids()
    for news in new_news:
        for user_id in user_ids:
            print(user_id)
            try:
                if news.img is None:
                    bot.send_message(user_id, news.to_telegram_message(), parse_mode='HTML', disable_web_page_preview=True)
                else:
                    bot.send_photo(user_id, photo=news.img, caption=news.to_telegram_message(), parse_mode='HTML')
            except:
                print("An exception occurred in sending message to user ", user_id)

    print("finish polling_function")


def poll_infinity(waiter):
    while True:
        polling_function()
        time.sleep(waiter)


threading.Thread(target=poll_infinity, args=(60,)).start()

bot.infinity_polling()
