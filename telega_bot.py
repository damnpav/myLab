import telebot
from telebot import types
import time
import os
import re
from datetime import datetime
import traceback

bot_token = open('/home/jet/Документы/telega_api.txt').readline()[:-1]
test_chat_id = '305402034'
path_to_replied_id = 'replied_id.txt'


def cor_calc(tickers_str):
    tickers_list = tickers_str.replace(' ', '').split(',')
    if len(tickers_list) < 2:
        return "Incorrect request. String should be in format like: 'AMZN, MSFT'. If you don't know share's " \
               "ticker - use ticker searcher."
    from models import correlation_calc as cc
    return cc(tickers_list).to_string()


def welcoming_buttons():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Model portfolio', callback_data='model_cb'),
               types.InlineKeyboardButton(text='Correlation radar', callback_data='corr_calc_cb'),
               types.InlineKeyboardButton(text='Ticker searcher', callback_data='searcher_cb'),
               types.InlineKeyboardButton(text='About project', callback_data='about'),
               types.InlineKeyboardButton(text='Contact us', callback_data='contact'))
    return markup


class Session:
    def __init__(self, bot_token):
        self.bot = telebot.TeleBot(bot_token)  # initialize bot
        self.replied_list = open(path_to_replied_id).read().split('\n')  # list with answered messages id
        self.received_list = self.bot.get_updates()     # get list of updates

    def reply_to_message(self, message, message_id, chat_id):
        self.bot.send_message(chat_id=chat_id, text='<pre> ' + message + ' </pre>',
                              reply_to_message_id=message_id, parse_mode='HTML')

    def send_buttons(self, message, chat_id, buttons):
        self.bot.send_message(chat_id=chat_id, text=message, reply_markup=buttons,
                              parse_mode='HTML')

    def send_message(self, message, chat_id):
        self.bot.send_message(chat_id=chat_id, text=message, parse_mode='HTML')


def main(bot_token):
    new_session = Session(bot_token)
    for el in new_session.received_list:
        another_dict = eval(str(el).replace('<', '"').replace('>', '"'))  # parse collected messages to dict

        # avoid edited messages
        if another_dict['edited_message'] is not None:
            continue

        if el.callback_query:
            message_id = str(el.callback_query.message.json['message_id'])
            message_text = str(el.callback_query.data)
            your_chat_id = str(el.callback_query.message.chat.id)
        else:
            message_id = str(another_dict['message']['json']['message_id'])
            message_text = str(another_dict['message']['text'])
            your_chat_id = str(another_dict['message']['json']['chat']['id'])

        # avoid answered messages
        if message_id in new_session.replied_list:
            continue

        if re.search(r'start', message_text):
            new_session.send_buttons('Welcome to PavlinLab! \n Choose your option:', your_chat_id, welcoming_buttons())
        elif re.search(r'model_cb', message_text):
            new_session.send_message('For creating model of your portfolio please type command \n//model and write '
                                     'tickers of shares that you want to include in your portfolio, sep by comma. '
                                     '\n\nFor example:\n //model AMD, AMZN, MSFT, BK, AAPL\n\n'
                                     'You may search for ticker of your company with //search command.', your_chat_id)
        with open(path_to_replied_id, 'a') as replied_id_file:
            replied_id_file.write(message_id + '\n')  # save id of aswered message
    del new_session  # clear class


while not os.path.isfile('/home/jet/Документы/myLab/bot_stop.txt'):
    try:
        main(bot_token)
    except Exception as e:
        print(traceback.format_exc())
        with open('log.txt', 'a') as log_file:
            log_file.write(str(e) + ': ' + str(traceback.format_exc()) + ' - ' +
                           datetime.now().strftime("%Y-%m-%d %H:%M") + '\n\n')
        pass
    time.sleep(10)


#main(bot_token)

