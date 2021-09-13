import pandas as pd
import numpy as np
import yfinance as yf
from matplotlib import pyplot as plt

# mean-variance analysis
# it's day-to-day model, also let's try month-to-month and year-to-year and compare results
# TODO visualisation tool
# TODO: set restrictions
#  Using the Public API (without authentication), you are limited to 2,000 requests per hour per IP
#  (or up to a total of 48,000 requests a day).
class Portfolio:
    def __init__(self, shares, quantity, start_prices, start_dates):
        self.shares = shares            # list with share names
        self.share_data = yf.download(  # download Df with historical data
                                        tickers=" ".join(shares),
                                        period="max",
                                        interval="1d",
                                        group_by='ticker',
                                        auto_adjust=True,
                                        prepost=True,
                                        threads=True,
                                        proxy=None)
        self.return_df = pd.DataFrame()
        self.stdevs = {}
        self.current_values = {}

        k = 0
        for share in self.shares:  # adding log return
            if len(self.shares) == 1:
                self.share_data['Log_ret'] = np.log(self.share_data['Close']) - \
                                                      np.log(self.share_data['Close'].shift(1))
                self.return_df[share] = self.share_data['Log_ret']
                self.stdevs[share] = np.std(self.share_data['Log_ret'])
                self.current_values[share] = self.share_data['Close'][-1] * quantity[k]
            else:
                self.share_data[(share, 'Log_ret')] = np.log(self.share_data[(share, 'Close')]) -\
                                                  np.log(self.share_data[(share, 'Close')].shift(1))
                self.return_df[share] = self.share_data[(share, 'Log_ret')]
                self.stdevs[share] = np.std(self.share_data[(share, 'Log_ret')])
                self.current_values[share] = self.share_data[(share, 'Close')][-1] * quantity[k]
            k += 1

        self.quantity = quantity    # list with share quantity
        self.start_prices = start_prices    # list with share buy prices
        self.start_dates = start_dates  # list with share start dates
        self.total_value = sum(self.current_values.values())  # total value of portfolio

        self.weights = {}
        self.exp_ret = {}  # expected return per share
        self.portfolio_exp_ret = 0  # expected return of portfolio
        for share in self.shares:
            self.weights[share] = self.current_values[share] / self.total_value  # calculate weights
            if len(self.shares) == 1:
                self.exp_ret[share] = self.share_data['Log_ret'].mean()
            else:
                self.exp_ret[share] = self.share_data[(share, 'Log_ret')].mean()
            self.portfolio_exp_ret += self.weights[share] * self.exp_ret[share]

        self.corr_coef = self.return_df.corr()  # correlation matrix

        self.general_variance = 0
        for share_i in self.shares:
            for share_j in self.shares:
                self.general_variance += self.weights[share_i] * self.weights[share_j] * \
                                         self.stdevs[share_i] * self.stdevs[share_j] * \
                                         self.corr_coef[share_i][share_j]

    # TODO need to test
    def portfolio_return(self, quantity):
        portfolio_ret_calc = 0  # expected return of portfolio
        weights_calc = {}
        exp_ret_calc = {}
        k = 0
        for share in self.shares:
            weights_calc[share] = quantity[k]  # calculate weights
            portfolio_ret_calc += weights_calc[share] * self.exp_ret[share]
            k += 1

        general_variance_calc = 0
        for share_i in self.shares:
            for share_j in self.shares:
                general_variance_calc += weights_calc[share_i] * weights_calc[share_j] * \
                                         self.stdevs[share_i] * self.stdevs[share_j] * \
                                         self.corr_coef[share_i][share_j]

        return portfolio_ret_calc, general_variance_calc


# myPortfolio = Portfolio(['AMD', 'KO', 'SAVE'], [1, 1, 1], [1, 1, 1], [1, 1, 1])
# print(myPortfolio.stdevs)
# print(myPortfolio.corr_coef)
#
# plt.figure()
# sr = myPortfolio.share_data[('AMD', 'Close')]
# sr.plot(title='AMD prices')
# plt.show()


#  TODO
# Portfolio optimisation
# Recommendational system: too high correlation, higher\ lower than MA and so on

def correlation_calc(shares):
    """
    Get a correlation matrix from list of tickers
    :param shares: list with tickers
    :return: correlation matrix
    """
    share_data = yf.download(  # download Df with historical data
                                        tickers=" ".join(shares),
                                        period="max",
                                        interval="1d",
                                        group_by='ticker',
                                        auto_adjust=True,
                                        prepost=True,
                                        threads=True,
                                        proxy=None)
    return_df = pd.DataFrame()
    for share in shares:  # adding log return
        share_data[(share, 'Log_ret')] = np.log(share_data[(share, 'Close')]) - \
                                         np.log(share_data[(share, 'Close')].shift(1))
        return_df[share] = share_data[(share, 'Log_ret')]
    corr_coef_log_ret = return_df.corr()
    return corr_coef_log_ret


# TODO
# need always to improve this search function
def ticker_searcher(company_name):
    """
    Search stock ticker by its company's name
    :param company_name: str
    :return: found ticket: str / Not Found / dataframe with matches
    """
    ticker_base = pd.read_csv('secwiki_tickers.csv')
    return_df = ticker_base.where(ticker_base['Name'].str.contains(company_name, case=False)).dropna()
    if len(return_df) == 1:
        return return_df['Ticker'].to_list()[0]
    elif len(return_df) == 0:
        return 'Not Found'
    else:
        return return_df[['Ticker', 'Name', 'Sector', 'Industry']]


def check_ticker(ticker):
    """
    Check if ticker exist at SPB Exchange
    :param ticker:
    :return:
    """
    securities_df = pd.read_csv('ListingSecurityList.csv', sep=';', engine='python')
    ticker_base = pd.read_csv('secwiki_tickers.csv')
    securities_list = securities_df['s_RTS_code'].to_list() + ticker_base['Ticker'].to_list()
    return ticker in securities_list




