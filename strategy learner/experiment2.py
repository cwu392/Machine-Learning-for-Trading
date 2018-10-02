import matplotlib.pyplot as plt
import datetime
import pandas as pd
import util as ut
import BagLearner as bl
import DTLearner as dt
import numpy as np
from marketsim import marketsim
import StrategyLearner as sl

def author(self):
    return 'cwu392'

if __name__ == '__main__':
    symbol = 'JPM'
    sd = datetime.datetime(2008, 1, 1)
    ed = datetime.datetime(2009, 12, 31)
    dates = pd.date_range(sd, ed)
    prices_all = ut.get_data([symbol], dates)  # automatically adds SPY


    prices = ut.get_data([symbol], pd.date_range(sd, ed))
    prices = prices[symbol]

    res = []
    num_trades = []
    impacts = [0, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5]
    for impact in impacts:
        learner = sl.StrategyLearner(verbose = False, impact = impact) # constructor
        learner.addEvidence(symbol = symbol, sd=sd, ed=ed, sv = 100000) # training phase
        df_trades = learner.testPolicy(symbol = symbol, sd=sd, ed=ed, sv = 100000) # testing phase
        num_trades.append(np.count_nonzero(df_trades))

        vals_ml = marketsim(df_trades, prices, impact = impact)

        vals_ml = vals_ml / vals_ml.ix[0]
        res.append(vals_ml)
    #print df_trades
    plt.xlabel('impact value')
    plt.ylabel('number of trades')
    plt.xticks(np.arange(len(impacts)), impacts)
    plt.plot(num_trades)
    plt.show()

    handles = []
    for i in range(len(impacts)):
        mlstrategy, = plt.plot(res[i], label = str(impacts[i]))
        handles.append(mlstrategy)
        #print res[-1]

    plt.legend(handles=handles, loc=2)
    plt.show()