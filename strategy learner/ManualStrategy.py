import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import datetime as dt
import types
import os
from util import get_data, plot_data
from marketsim import marketsim

def author(self):
    return 'cwu392'

def testPolicy(symbol = 'JPM', sd = dt.datetime(2008, 1, 1), ed = dt.datetime(2009, 12, 31), sv = 100000):
    syms=[symbol]
    window_size = 20
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    norm_prices=prices.divide(prices.ix[0])
    df_trades = prices_all[syms].copy()  # only portfolio symbols
    df_trades.values[:, :] = 0
    current = 0

    # Add My Indicators: SMA,BB,Momentum
    #1. SMA:
    smap=norm_prices.copy()
    smap['SMA/P']=prices.rolling(window_size).mean()/prices

    #2. BB: Bollinger Band Index
    bb=norm_prices.copy()
    bb['SMA']=norm_prices.rolling(window_size).mean()
    bb['STD']=norm_prices.rolling(window_size).std()
    bb['Upper BB']=bb['SMA']+2.0*bb['STD']
    bb['Lower BB']=bb['SMA']-2.0*bb['STD']
    bb['BBI']=(bb.ix[:, 0]-bb['Lower BB'])/(bb['Upper BB']-bb['Lower BB'])

    #3. MM: Momentum
    MM = norm_prices.copy()
    MM['Momentum'] = MM.divide(MM.shift(window_size)) - 1

    #Normalization
    smap['SMA/P'] = (smap['SMA/P']-smap['SMA/P'].mean())/smap['SMA/P'].std()
    bb['BBI'] = (bb['BBI']-bb['BBI'].mean())/bb['BBI'].std()
    MM['Momentum'] = (MM['Momentum']-MM['Momentum'].mean())/MM['Momentum'].std()
    
    for i in range(window_size, len(prices.index)):
        # My Strategy:
        ## 1. When should you buy: BB, Momentum, SMA:
        if (smap['SMA/P'][i]>bb['BBI'][i]) and (MM['Momentum'][i]<-0.25):
            df_trades.values[i, :] = 1000 - current
            current = 1000
        ## 2. When should you sell: BB, SMA:
        elif (smap['SMA/P'][i]<bb['BBI'][i]) and (MM['Momentum'][i]>0.25):
            df_trades.values[i, :] = -1000 - current
            current = -1000

    return df_trades