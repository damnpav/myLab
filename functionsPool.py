import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
import mysql.connector


#  df = pd.read_csv(r'C:\Users\hcani\Documents\GitHub\myLab\marketData\ANA.MC.csv')  # your df
# TODO debug candles
# think about figures and seaborn objectes for GUI
def candles(yourTitle, xTitle, yTitle, dataFrame):
    """
    Function for building market figures, returning figure object
    :param yourTitle: Title of graph
    :param xTitle: Title of X axis
    :param yTitle: Title of Y axis
    :param dataFrame: source DataFrame with columns Date, Open, High, Low, Close
    :return: figure object
    """
    fig = go.Figure(data = go.Ohlc(x = dataFrame['Date'],
                                   open = dataFrame['Open'],
                                   high = dataFrame['High'],
                                   low = dataFrame['Low'],
                                   close = dataFrame['Close']))
    fig.update_layout(title_text= yourTitle,
                      title={
                        'y':0.9,
                        'x':0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'},
                      xaxis_rangeslider_visible=True, xaxis_title= xTitle, yaxis_title= yTitle)
    return fig

# TODO optimisate that crap
def tics(linewidth, dataFrame, stockName):
    sns.set(style = "whitegrid")
    data = pd.DataFrame(list(dataFrame['Close'].values), list(dataFrame['Date'].values), columns = [stockName])
    sns.lineplot(data = data, palette = 'tab10', linewidth = linewidth)

pathToPass = r"C:\Users\hcani\Documents\MySQL Settings\sql_key.txt"
password = open(pathToPass).readlines()[0]
def getDf(stockId, password):
    cnx = mysql.connector.connect(user='root', password=password, host='127.0.0.1', database='stocks')
    cursor = cnx.cursor()
    query = ("SELECT * FROM ibexdata WHERE id = " + str(stockId))
    df = pd.read_sql(query, con = cnx)
    cnx.close()
    return df

df = getDf(0, password)
print(1)
fig = candles('AMC', 'Date', 'Price', df)
fig.show()