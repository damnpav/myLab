import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from visualize_models import visualise_models

market_data = yf.download(tickers=" ".join(['^GSPC', 'AAPL']), period='5y', interval='1d', group_by='ticker',
                          auto_adjust=True, prepost=True, threads=True, proxy=None)

x_sp = np.array(market_data['^GSPC']['Close']).reshape((-1, 1))
y_aapl = np.array(market_data['AAPL']['Close'])

model = LinearRegression()
model.fit(x_sp, y_aapl)
r_sq = model.score(x_sp, y_aapl)
print('coefficient of determination:', r_sq)

print('intercept:', model.intercept_)
print('slope:', model.coef_)

y_pred = model.predict(x_sp)
print('predicted response:', y_pred, sep='\n')

x_test = market_data['^GSPC']['Close']

visualise_models(x_test, y_aapl, y_pred)

result_df = pd.DataFrame(columns=['SP500', 'AAPL', 'predAAPL'])
result_df['SP500'] = np.log(market_data['^GSPC']['Close']) - np.log(market_data['^GSPC']['Close'].shift(1))
result_df['AAPL'] = np.log(market_data['AAPL']['Close']) - np.log(market_data['AAPL']['Close'].shift(1))
result_df['predAAPL'] = list(y_pred)
result_df['predAAPL'] = np.log(result_df['predAAPL']) - np.log(result_df['predAAPL'].shift(1))

df_cumsum = result_df.cumsum()

plt.figure(); df_cumsum.plot(); plt.legend(loc='best')
plt.show()


