"""MC1-P2: Optimize a portfolio."""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from util import get_data, plot_data
import scipy.optimize as spo


def get_portfolio_value(prices,allocs):
    normed=prices/prices.ix[0,:]
    alloced=normed*allocs
    port_val=alloced.sum(axis=1)
    return port_val

def get_portfolio_status(port_val):
    sf=252.0
    rfr=0.0

    daily_rets=port_val.copy()
    daily_rets[1:]=(daily_rets[1:]/daily_rets[:-1].values)-1
    daily_rets=daily_rets[1:]

    cum_ret=(port_val[-1]/port_val[0])-1
    
    avg_daily_ret=daily_rets.mean()
    std_daily_ret=daily_rets.std()
    sharp_ratio=np.sqrt(sf)*(np.mean(daily_rets-rfr)/daily_rets.std())

    return cum_ret, avg_daily_ret, std_daily_ret, sharp_ratio

def find_optimum_allocs(prices): 
    Cguess= 1.0/prices.shape[1]
    function_Cguess=[Cguess]*prices.shape[1]
    cons = ({'type':'eq','fun':lambda function_Cguess: 1.0-np.sum(function_Cguess)})
    bnds = [(0,1) for x in prices.columns]
    result = spo.minimize(error_optimal_allocs, function_Cguess, args = (prices,), method='SLSQP', bounds = bnds, constraints = cons, options={'disp':True})
    allocs=result.x
    return allocs

def error_optimal_allocs(allocs,prices):
    port_val = get_portfolio_value(prices,allocs)
    cum_ret, avg_daily_ret, std_daily_ret, sharp_ratio = get_portfolio_status(port_val)
    error = std_daily_ret
    return error

def optimize_portfolio(sd, ed, syms, gen_plot = True):
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY

    prices_all.fillna(method="ffill",inplace=True)
    prices_all.fillna(method="bfill",inplace=True)

    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    allocs = find_optimum_allocs(prices)
    allocs = allocs/np.sum(allocs)

    port_val = get_portfolio_value(prices,allocs)
    cum_ret, avg_daily_ret, std_daily_ret, sharp_ratio = get_portfolio_status(port_val)

    normed_SPY = prices_SPY/prices_SPY.ix[0,:]
    if gen_plot:
        df_temp = pd.concat([port_val, normed_SPY], keys=['Portfolio', 'SPY'], axis=1)
        plot_data(df_temp, title='Daily Portfolio Value and SPY')
        pass

    return allocs, cum_ret, avg_daily_ret, std_daily_ret, sharp_ratio

def test_code():
    # This function WILL NOT be called by the auto grader
    # Do not assume that any variables defined here are available to your function/code
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!

    start_date = dt.datetime(2008,6,1)
    end_date = dt.datetime(2009,6,1)
    symbols = ['IBM', 'X', 'GLD']

    # Assess the portfolio
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date, syms = symbols, gen_plot = True)

    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr

if __name__ == "__main__":
    # This code WILL NOT be called by the auto grader
    # Do not assume that it will be called
    test_code()