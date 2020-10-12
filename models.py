import pandas as pd
import numpy as np
import yfinance as yf
#from matplotlib import pyplot as plt

# mean-variance analysis
# it's day-to-day model, also let's try month-to-month and year-to-year and compare results
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
            self.exp_ret[share] = self.share_data[(share, 'Log_ret')].mean()
            self.portfolio_exp_ret += self.weights[share] * self.exp_ret[share]

        self.corr_coef = self.return_df.corr()  # correlation matrix

        self.general_variance = 0
        for share_i in self.shares:
            for share_j in self.shares:
                self.general_variance += self.weights[share_i] * self.weights[share_j] * \
                                         self.stdevs[share_i] * self.stdevs[share_j] * \
                                         self.corr_coef[share_i][share_j]

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
        return return_df





