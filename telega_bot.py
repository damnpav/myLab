import telebot
import pandas as pd
import re

bot_token = open('/home/jet/Документы/telega_api.txt').readline()[:-1]


class Session:
    def __init__(self, bot_token):
        self.bot = telebot.TeleBot(bot_token)  # initialize bot
        self.received_list = self.bot.get_updates()     # get list of updates

    def cor_calc(self, tickers_str):
        tickers_list = tickers_str.replace(' ', '').split(',')
        if len(tickers_list) < 2:
            return "Incorrect request. String should be in format like: 'AMZN, MSFT'. If you don't know share's " \
                   "ticker - use ticker searcher."
        from models import correlation_calc as cc
        return cc(tickers_list).to_string()

    def reply_to_message(self, message, message_id, chat_id):
        self.bot.send_message(chat_id=chat_id, text='<pre> ' + message + ' </pre>',
                              reply_to_message_id=message_id, parse_mode='HTML',
                              disable_notification=self.DisableNotification)




