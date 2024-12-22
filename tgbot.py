import telebot, os

f = open("secrets.txt")
bot = telebot.TeleBot(f.readline())
f.close()

with open("data\\users", "r") as f:
    _subscribers = f.readlines()


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Вы подписались на хайлайты Кинкиллера! Спасибо!")
    with open("data\\users", "r") as f:
        t = f.read().splitlines()
        print(t)
    with open("data\\users", "a") as f:
        if str(message.chat.id) not in t:
            f.write(str(message.chat.id))


def video_spam(_video):
    _subscribers = ['-829467245']
    for x in _subscribers:
        bot.send_message(x, "Внимание! ХАЙЛАЙТ ДЕТЕКТЕД")
        with open(_video, 'rb') as video_file:
            bot.send_video(x.strip(), video_file, width=1920, height=1080)

for video in os.listdir("data/videos"):
    video_spam(f"data/videos/{video}")

bot.polling(none_stop=True, interval=0)

