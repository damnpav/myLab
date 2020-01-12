import pandas as pd
import plotly.graph_objects as go
import pyodbc

# TODO wrap it in function
df = pd.read_csv(r'C:\Users\hcani\Documents\GitHub\myLab\marketData\ANA.MC.csv')  # your df

def grapher(yourTitle, xTitle, yTitle, dataFrame):
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

# grapher('AMA.MC', 'Date', 'Price', df).show()

# write a function for selecting data from MySQL to dataframe from showing praphs