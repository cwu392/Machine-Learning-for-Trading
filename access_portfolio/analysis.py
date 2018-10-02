"""Analyze a portfolio."""

import pandas as pd
import numpy as np
import datetime as dt
from math import sqrt
from util import get_data, plot_data

# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality
def assess_portfolio(sd = dt.datetime(2008,1,1), ed = dt.datetime(2009,1,1), \
    syms = ['GOOG','AAPL','GLD','XOM'], \
    allocs=[0.1,0.2,0.3,0.4], \
    sv=1000000, rfr=0.0, sf=252.0, \
    gen_plot=False):

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    # Get daily portfolio value
    #port_val = prices_SPY # add code here to compute daily portfolio values
    normed=prices/prices.ix[0,:]
    alloced=normed*allocs
    pos_vals=alloced*sv
    port_val=pos_vals.sum(axis=1)
    daily_rets=port_val.copy()
    daily_rets[1:]=(daily_rets[1:]/daily_rets[:-1].values)-1
    daily_rets=daily_rets[1:]
    cum_ret=(port_val[-1]/port_val[0])-1
    avg_daily_ret=daily_rets.mean()
    std_daily_ret=daily_rets.std()
    sharp_ratio=sqrt(sf)*(np.mean(daily_rets-rfr)/daily_rets.std())

    # Get portfolio statistics (note: std_daily_ret = volatility)
    #cr, adr, sddr, sr = [0.25, 0.001, 0.0005, 2.1] # add code here to compute stats
    cr=cum_ret
    adr=avg_daily_ret
    sddr=std_daily_ret
    sr=sharp_ratio

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        pass

    # Add code here to properly compute end value
    #ev = sv
    ev=port_val[-1]

    return cr, adr, sddr, sr, ev

def test_code():
    # This code WILL NOT be tested by the auto grader
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!
    #start_date = dt.datetime(2009,1,1)
    #end_date = dt.datetime(2010,1,1)
    #symbols = ['GOOG', 'AAPL', 'GLD', 'XOM']
    #allocations = [0.2, 0.3, 0.4, 0.1]
    start_val = 1000000  
    risk_free_rate = 0.0
    sample_freq = 252

    #Case 1:
    #start_date = dt.datetime(2010,1,1)
    #end_date = dt.datetime(2010,12,31)
    #symbols = ['GOOG', 'AAPL', 'GLD', 'XOM']
    #allocations = [0.2, 0.3, 0.4, 0.1]

    #Case 2:
    #start_date = dt.datetime(2010,1,1)
    #end_date = dt.datetime(2010,12,31)
    #symbols = ['AXP', 'HPQ', 'IBM', 'HNZ']
    #allocations = [0.0, 0.0, 0.0, 1.0]

    #Case 3:
    start_date = dt.datetime(2010,6,1)
    end_date = dt.datetime(2010,12,31)
    symbols = ['GOOG', 'AAPL', 'GLD', 'XOM']
    allocations = [0.2, 0.3, 0.4, 0.1]


    # Assess the portfolio
    cr, adr, sddr, sr, ev = assess_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        allocs = allocations,\
        sv = start_val, \
        gen_plot = False)

    # Print statistics
    print("Start Date:", start_date)
    print("End Date:", end_date)
    print("Symbols:", symbols)
    print("Allocations:", allocations)
    print("Sharpe Ratio:", sr)
    print("Volatility (stdev of daily returns):", sddr)
    print("Average Daily Return:", adr)
    print("Cumulative Return:", cr)
    print("Ending Value", ev)

if __name__ == "__main__":
    test_code()