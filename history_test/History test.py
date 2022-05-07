import json
import logging
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

TOKEN = TOKEN

is_stop = False
end = False
is_start = True
first_time = True
number = 0

right_and_wrong = [0, 0]

with open('history_test.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)


def start(update, context):
    update.message.reply_text('Привет! Пройдешь тест по истории?')


def stop(update, context):
    global is_stop
    update.message.reply_text('До новых встреч!')
    is_stop = True


def first(update):
    update.message.reply_text(data['test'][number]['question'])


def echo(update, context):
    global number, end, is_stop, is_start, first_time, right_and_wrong
    if end is True:
        end = False
        is_stop = False
        start(update, context)
        number = -1
        right_and_wrong = [0, 0]
    if number == 9:
        is_stop = True
        update.message.reply_text(f'{right_and_wrong[0]} правильных из 10-ти')
        update.message.reply_text('Может еще раз?')
        end = True
    if not is_stop:
        if not first_time:
            if update.message.text == data['test'][number]['response']:
                right_and_wrong[0] += 1
            else:
                right_and_wrong[1] += 1
            number += 1
        if first_time:
            first_time = False
            update.message.reply_text(data['test'][number]['question'])
        else:
            if not is_stop:
                update.message.reply_text(data['test'][number]['question'])


def main():
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("stop", stop))

    text_handler = MessageHandler(Filters.text & ~Filters.command, echo)
    dp.add_handler(text_handler)
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()