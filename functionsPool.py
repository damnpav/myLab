import pandas as pd
import numpy as np
import plotly.graph_objects as go
#TODO wrap it in function
df = pd.read_csv(r'C:\Users\hcani\Documents\GitHub\myLab\marketData\ANA.MC.csv')  # your df
yourTitle = 'Test graph'
xTitle = 'xTitle'
yTitle = 'yTitle'

fig = go.Figure(data = go.Ohlc(x = df['Date'],
                               open = df['Open'],
                               high = df['High'],
                               low = df['Low'],
                               close = df['Close']))
fig.update_layout(title_text= yourTitle,
                  title={
                    'y':0.9,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                  xaxis_rangeslider_visible=True, xaxis_title= xTitle, yaxis_title= yTitle)
fig.show()