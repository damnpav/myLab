import pandas as pd
import yfinance as yf
from datetime import datetime as dt
import dataframe_image as dfi

# TODO 1: extreme change +
# TODO 2: extreme volumes - need in base
# TODO 3: deploy
# TODO 4: extreme volatility +
# TODO 5: functions for absolute values for month\ year and calendar month\ year
# TODO 6: include company name to final table and share type

stock_list = pd.read_csv('ListingSecurityList.csv', sep=';', encoding='windows-1251')
rus_description = {'s_level_name': 'Раздел списка', 'e_full_name': 'Полное имя', 'e_INN_code': 'ИНН',
                   's_sec_type_name_dop': 'Вид ц.б.', 's_sec_form_name_full': 'Категория ц.б.', 's_RTS_code': 'Тикер',
                   's_ISIN_code': 'ISIN', 'si_gos_reg_num': 'Гос.номер', 'si_gos_reg_date': 'Дата гос.номера',
                   's_face_value': 'Номинальная стоимость', 's_face_value_currency': 'Валюта',
                   's_quot_list_in_date': 'Дата включения', 's_segment': 'Сегмент списка',
                   's_date_defolt': 'Дата дефолта', 's_date_technic_defolt': 'Дата тех. дефолта'}

stock_list = stock_list.rename(columns=rus_description)
stock_list['Тикер'] = stock_list['Тикер'].str.replace('@', '.')
requested_stocks = stock_list[(stock_list['Валюта'] == 'USD') | (stock_list['Валюта'] == 'EUR')]['Тикер'][:100]

share_data = yf.download(tickers=' '.join(list(requested_stocks)), period='1d', interval="1d", group_by='ticker',
                         auto_adjust=True, prepost=True, threads=True, proxy=None)

results_df = pd.DataFrame(columns=['Ticker', 'Close/Open', 'High/Low', 'Volume', 'Name', 'Type'])

current_values = dict.fromkeys(results_df.columns)
for stock in requested_stocks:
    current_values['Ticker'] = stock
    current_values['Close/Open'] = (share_data[stock]['Close'] / share_data[stock]['Open']).values[0]
    current_values['High/Low'] = (share_data[stock]['High'] / share_data[stock]['Low']).values[0]
    current_values['Volume'] = (share_data[stock]['Volume']).values[0]
    current_values['Name'] = stock_list[stock_list['Тикер'] == stock]['Полное имя'].values[0]
    current_values['Type'] = stock_list[stock_list['Тикер'] == stock]['Вид ц.б.'].values[0]
    results_df = results_df.append(current_values, ignore_index=True)

top_surge = results_df.sort_values(by='Close/Open', ascending=False)
top_fall = results_df.sort_values(by='Close/Open', ascending=True)
top_volatility = results_df.sort_values(by='High/Low')
top_volume = results_df.sort_values(by='Volume')

corr_path = f'PNGs/top_surge_df_{dt.now().strftime("%H%M%S%d%m%Y")}.png'
dfi.export(top_surge[:30], corr_path, table_conversion='matplotlib')

