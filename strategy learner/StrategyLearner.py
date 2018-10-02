"""
Template for implementing StrategyLearner  (c) 2016 Tucker Balch
"""

import datetime as dt
import pandas as pd
import util as ut
import BagLearner as bl
#import QLearner as ql
import DTLearner as dl
import numpy as np
import random

class StrategyLearner(object):

    # constructor
    def __init__(self, verbose = False, impact=0.0):
        self.verbose = verbose
        self.impact = impact
        self.window_size=20
        self.feature_size = 5
        self.N = 10
        bag=20
        leaf_size = 5
        self.learner=bl.BagLearner(learner=dl.DTLearner, bags=bag, kwargs={"leaf_size":leaf_size})

    def author(self):
        return 'cwu392'

    # this method should create a QLearner, and train it for trading
    def addEvidence(self, symbol = "IBM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,1,1), \
        sv = 10000): 

        # add your code to do learning here
        window_size=self.window_size
        feature_size = self.feature_size
        N = self.N
        impact=self.impact
        threshold = max(0.05, 2 * impact)
        # example usage of the old backward compatible util function
        syms=[symbol]
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        norm_prices=prices.divide(prices.ix[0])
        #prices_SPY = prices_all['SPY']  # only SPY, for comparison later
        #if self.verbose: print prices
  
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
        # smap['SMA/P'] = (smap['SMA/P']-smap['SMA/P'].mean())/smap['SMA/P'].std()
        # bb['BBI'] = (bb['BBI']-bb['BBI'].mean())/bb['BBI'].std()
        # MM['Momentum'] = (MM['Momentum']-MM['Momentum'].mean())/MM['Momentum'].std()
        
        X_train=[]
        Y_train=[]

        for i in range(window_size + feature_size + 1, len(prices) - N):
            X_train.append( np.concatenate( (smap['SMA/P'][i - feature_size : i], bb['BBI'][i - feature_size : i], MM['Momentum'][i - feature_size : i]) ) )
            ret= (prices.values[i + N] - prices.values[i]) / prices.values[i]
            #Cal. N days return
            if ret > threshold:
                Y_train.append(1)
            elif ret < -threshold:
                Y_train.append(-1)
            else:
                Y_train.append(0)

        X_train=np.array(X_train)
        Y_train=np.array(Y_train)

        self.learner.addEvidence(X_train, Y_train)
    # this method should use the existing policy and test it against new data
    def testPolicy(self, symbol = "IBM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):

        current_holding=0

        # here we build a fake set of trades
        # your code should return the same sort of data
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data([symbol], dates)  # automatically adds SPY
        trades = prices_all[[symbol,]]  # only portfolio symbols
        trades_SPY = prices_all['SPY']  # only SPY, for comparison later

        window_size=self.window_size
        feature_size = self.feature_size
        N=self.N

        syms=[symbol]
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        norm_prices=prices.divide(prices.ix[0])

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

        trades.values[:, :] = 0
        Xtest = []

        for i in range(window_size + feature_size + 1, len(prices) - N):
            data = np.concatenate( (smap['SMA/P'][i - feature_size : i], bb['BBI'][i - feature_size : i], MM['Momentum'][i - feature_size : i]) )
            Xtest.append(data)

        res = self.learner.query(Xtest)

        for i, r in enumerate(res):
            if r > 0:
                # Buy signal
                trades.values[i + window_size + feature_size + 1, :] = 1000 - current_holding
                current_holding = 1000
            elif r < 0:
                # Sell signal
                trades.values[i + window_size + feature_size + 1, :] = - 1000 - current_holding
                current_holding = -1000

        if self.verbose: print type(trades) # it better be a DataFrame!
        if self.verbose: print trades
        if self.verbose: print prices_all
        return trades

if __name__=="__main__":
    print "One does not simply think up a strategy"