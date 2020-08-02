import pandas as pd
import numpy as np
import yfinance as yf
from matplotlib import pyplot as plt


class Portfolio:
    def __init__(self, shares, quantity, start_prices, start_dates):
        self.shares = shares            # list with share names
        self.share_data = yf.download(  # download Df with historical data
                                        tickers=" ".join(shares),
                                        period="max",
                                        interval="1d",
                                        group_by='ticker',
                                        #auto_adjust=True,
                                        prepost=True,
                                        threads=True,
                                        proxy=None)
        self.stdevs = {}
        self.current_values = {}
        k = 0
        for share in self.shares:  # adding log return
            self.share_data[(share, 'Log_ret')] = np.log(self.share_data[(share, 'Close')]) -\
                                             np.log(self.share_data[(share, 'Close')].shift(1))
            self.stdevs[share] = np.std(self.share_data[(share, 'Log_ret')])
            self.current_values[share] = self.share_data[(share, 'Close')][-1] * quantity[k]

        self.quantity = quantity    # list with share quantity
        self.start_prices = start_prices    # list with share buy prices
        self.start_dates = start_dates  # list with share start dates
        self.total_value = sum(self.current_values.values())  # total value of portfolio

        self.weights = {}
        corr_data = []  # collecting data for correlation analysis
        for share in self.shares:
            self.weights[share] = self.current_values[share] / self.total_value
            corr_data.append(self.share_data[(share, 'Close')])
        self.corr_coef = np.corrcoef(corr_data)


myPortfolio = Portfolio(['AMD', 'KO', 'SAVE'], [1, 1, 1], [1, 1, 1], [1, 1, 1])
print(myPortfolio.stdevs)
print(myPortfolio.corr_coef)

plt.figure()
sr = myPortfolio.share_data[('AMD', 'Close')]
sr.plot(title='AMD prices')
plt.show()



