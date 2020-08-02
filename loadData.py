import pandas as pd
import yfinance as yf
from sqlalchemy import create_engine
rtsi_df = pd.read_excel('rtsi_filled.xlsx')

engine = create_engine('mysql+pymysql://root:Slim171072Shady!@localhost:3306/indexes')
conn = engine.connect()

#conn.execute("INSERT INTO RTSI_keys VALUES (0, 'APPLE', N'ЯБЛОКО', N'Яблочная компания')")

conn.close()
engine.dispose()

for i in range(len(rtsi_df)):
    stock_name = str(rtsi_df['Share'][i])
    stock_descr = ''
    if str(rtsi_df['base'][i]) == '+':


