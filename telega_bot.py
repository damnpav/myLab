import telebot
from telebot import types
import time
import os
import re
from datetime import datetime
import traceback
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import models


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
    # how to send
    #my_bot.send_photo(chat_id=test_chat_id, photo=foto, caption='Portf_picture', parse_mode='HTML')


def welcoming_buttons():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Portfolio', callback_data='model_cb'),
               types.InlineKeyboardButton(text='Correlations', callback_data='corr_calc_cb'),
               types.InlineKeyboardButton(text='Find ticker', callback_data='searcher_cb'),
               types.InlineKeyboardButton(text='About', callback_data='about'),
               types.InlineKeyboardButton(text='Contact us', callback_data='contact'))
    return markup


def print_out_model(shares, quantity):
    for share in shares:
        if not models.check_ticker(share):
            return f'{share} ticker not found at our base. Temporally we use only tickers from SPB Stock Exchange.' \
                   f'You may search for ticker of your company with /search command.'
    portf = models.Portfolio(shares, quantity, [1]*len(shares), [1]*len(shares))
    return_str = f'Expectation return: {round(portf.portfolio_exp_ret*253*100, 2)} % annually.' \
                 f'Risk: {round(portf.general_variance*253*100, 2)} % annually.' \
                 f'Risk\ Reward ratio: {round(portf.general_variance/portf.portfolio_exp_ret, 2)}'


def weights_pie(weights, pie_name):
    labels = list(weights.keys())
    sizes = list(weights.values())
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig(pie_name)


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
    get_message = False  # flag for controlling loop time for using and non-using period
    new_session = Session(bot_token)
    for el in new_session.received_list:
        another_dict = eval(str(el).replace('<', '"').replace('>', '"'))  # parse collected messages to dict

        # avoid edited messages
        if another_dict['edited_message'] is not None:
            continue

        update_id = str(el.update_id)
        # avoid answered messages
        if update_id in new_session.replied_list:
            continue

        if el.callback_query:
            message_id = str(el.callback_query.message.json['message_id'])
            message_text = str(el.callback_query.data)
            your_chat_id = str(el.callback_query.message.chat.id)
            username = str(el.callback_query.from_user.username)
        else:
            message_id = str(another_dict['message']['json']['message_id'])
            message_text = str(another_dict['message']['text'])
            your_chat_id = str(another_dict['message']['json']['chat']['id'])
            username = str(el.message.from_user.username)

        get_message = True  # flag for controlling loop time for using and non-using period

        if re.search(r'model_cb', message_text):
            new_session.send_message('For creating model of your portfolio please type command \n/model and write '
                                     'tickers of shares that you want to include in your portfolio, sep by comma. '
                                     '\n\nFor example:\n/model AMD, AMZN, MSFT, BK, AAPL\n\n'
                                     'You may search for ticker of your company with /search command.', your_chat_id)
        elif re.search(r'corr_calc_cb', message_text):
            new_session.send_message('To count correlation between some shares please type command \n/correlation '
                                     'and write tickers of these papers, sep by comma.'
                                     '\n\nFor example: \n/correlation INTC, CSCO, FB\n\n'
                                     'You may search for ticker of your company with /search command.', your_chat_id)
        elif re.search(r'searcher_cb', message_text):
            new_session.send_message('You may search for ticker of your company with /search command.\n\n'
                                     'For example: \n/search Xerox', your_chat_id)
        elif re.search(r'about', message_text):
            new_session.send_message('PavlinLab Project is a tool for modelling portfolio of securities '
                                     'with Modern Portfolio Theory.', your_chat_id)
        elif re.search(r'contact', message_text):
            new_session.send_message('You may always contact us on e-mail: hcanilvap@gmail.com', your_chat_id)
        else:
            new_session.send_buttons('Welcome to PavlinLab! \n Choose your option:', your_chat_id, welcoming_buttons())

        with open(path_to_replied_id, 'a') as replied_id_file:
            replied_id_file.write(update_id + '\n')  # save id of answered message
        with open('log.txt', 'a') as log_file:
            log_file.write(f'Username: {username}, Message_id: {message_id}, Message_text: {message_text}, '
                           f'Chat_id: {your_chat_id}, time: {datetime.now().strftime("%Y-%m-%d %H:%M")} \n\n')
    del new_session  # clear class
    return get_message


while not os.path.isfile('/home/jet/Документы/myLab/bot_stop.txt'):
    t = 15
    try:
        answer_flag = main(bot_token)
        if answer_flag:
            t = 5   # reducing answer time when bot have conversation
    except Exception as e:
        print(traceback.format_exc())
        with open('log.txt', 'a') as log_file:
            log_file.write(str(e) + ': ' + str(traceback.format_exc()) + ' - ' +
                           datetime.now().strftime("%Y-%m-%d %H:%M") + '\n\n')
        pass
    time.sleep(t)


#main(bot_token)

