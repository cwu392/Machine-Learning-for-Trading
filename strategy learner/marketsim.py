"""MC2-P1: Market simulator."""

import pandas as pd
import numpy as np
import datetime as dt
import os
import util as ut
import math

def author(self):
    return 'cwu392'

def marketsim(df_trades, prices, start_val = 1000000, share=0, commission=0, impact=0):
    df_holdings=pd.DataFrame(data=np.ones(len(prices))*share,index=prices.index,columns=['val'])
    df_cash=pd.DataFrame(data=np.ones(len(prices))*start_val,index=prices.index,columns=['val'])
    for i in range(0,len(prices.index)):
        cash_change = 0
        if df_trades.values[i][0]>0:
            sign=1
        else:
            sign=-1

        if df_trades.values[i][0]!=0:
            cash_change=(sign+impact)*abs(df_trades.values[i][0]*prices.values[i])
            cash_change=cash_change+commission
            #Commission always =0
        if i==0:
            df_cash['val'].iloc[i]=df_cash['val'].iloc[i]-cash_change
            df_holdings['val'].iloc[i]=df_holdings['val'].iloc[i]+df_trades.values[i][0]
            continue
        df_cash['val'].iloc[i] = df_cash['val'].iloc[i-1]-cash_change
        df_holdings['val'].iloc[i] = df_holdings['val'].iloc[i-1]+df_trades.values[i][0]

    df_share_val=df_holdings.val*prices
    portvals=df_share_val+df_cash.val
    return portvals

def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/my_strategy.csv"
    sv = 100000
    stock='JPM'

    # Process orders
    portvals = marketsim(orders_file = of, start_val = sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]] # just get the first column
    else:
        "warning, code did not return a DataFrame"
    
    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    
    #Training
    start_date = dt.datetime(2008,1,1)
    end_date = dt.datetime(2009,12,31)

    #Testing
    # start_date = dt.datetime(2010,1,1)
    # end_date = dt.datetime(2011,12,31)    

    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = ut.get_portfolio_stats(portvals)

    dates = pd.date_range(start_date, end_date)
    benchmark_pd=ut.get_data([stock], dates)

    trade_date=benchmark_pd.index[0]
    f=open('./orders/benchmark.csv','w')
    f.write("Date,Symbol,Order,Shares\n") # create the same file for marketsim.py
    f.write("{},{},BUY,1000\n".format(str(trade_date),stock))
    f.close()

    of_benchmark = "./orders/benchmark.csv"
    benchmark_portvals = compute_portvals(orders_file = of_benchmark, start_val = sv)
    if isinstance(benchmark_portvals, pd.DataFrame):
        benchmark_portvals = benchmark_portvals[benchmark_portvals.columns[0]] # just get the first column
    else:
        "warning, code did not return a DataFrame"
    
    # Get BenchMark portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    bm_cum_ret, bm_avg_daily_ret, bm_std_daily_ret, bm_sharpe_ratio = ut.get_portfolio_stats(benchmark_portvals)


    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)

    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Manual Portfolio Value: {}".format(portvals[-1])

    # print "Sharpe Ratio of BenchMark : {}".format(bm_sharpe_ratio)
    # print "Cumulative Return of BenchMark : {}".format(bm_cum_ret)
    # print "Standard Deviation of BenchMark : {}".format(bm_std_daily_ret)
    # print "Average Daily Return of BenchMark : {}".format(bm_avg_daily_ret)
    # print "BenchMark Portfolio Value: {}".format(benchmark_portvals[-1])


if __name__ == "__main__":
    test_code()
    #compute_portvals()
    #print marketsim.author