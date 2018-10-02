"""MC2-P1: Market simulator."""

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data
import math

def compute_portvals(orders_file = "./orders/orders-03.csv", start_val = 1000000, commission=0, impact=0):
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input
    # TODO: Your code here

    # In the template, instead of computing the value of the portfolio, we just
    # read in the value of IBM over 6 months

    orders_df = pd.read_csv(orders_file, index_col='Date', parse_dates=True, na_values=['nan'])
    orders_df = orders_df.sort_index() # Make Date Order Correct #
    dates=orders_df.index
    #dates=dates.drop_duplicates(keep='last')
    
    #print orders_df
    ## df_prices ##
    symbols=[]
    for i in range(0,len(orders_df.Symbol)):
        symbols.append(orders_df.Symbol[i])
    symbols=list(set(symbols))

    start_date=dates[0]
    end_date=dates[-1]
    index_dates=pd.date_range(start_date,end_date)
    REF_vals=get_data(symbols,index_dates,addSPY=True,colname='Adj Close')
    index_dates=REF_vals.index

    df_prices=pd.DataFrame(index=index_dates)
    df_prices=get_data(symbols,index_dates,addSPY=True,colname='Adj Close')
    df_prices.dropna(inplace=True)
    df_prices.fillna(method="ffill",inplace=True)
    df_prices.fillna(method="bfill",inplace=True)
    df_prices=df_prices[symbols] ##Remove SPY
    #df_prices['CASH']=pd.Series(1.0, index=dates)
    df_prices['CASH']=1.0

    #print df_prices

    ## df_trades ##
    df_trades=pd.DataFrame(0,index=index_dates,columns=symbols)
    #df_trades['CASH']=pd.Series(0, index=dates)
    df_trades['CASH']=0

    for i in range(0,len(orders_df)):
        if orders_df.Order[i]=='BUY':
            df_trades.loc[orders_df.index[i],orders_df.Symbol[i]]+=orders_df.Shares[i]
            df_trades.loc[orders_df.index[i],'CASH']+= -orders_df.Shares[i]*df_prices.loc[orders_df.index[i],orders_df.Symbol[i]]*(1+impact)-commission
        elif orders_df.Order[i]=='SELL':
            df_trades.loc[orders_df.index[i],orders_df.Symbol[i]]+=-orders_df.Shares[i]
            df_trades.loc[orders_df.index[i],'CASH']+= orders_df.Shares[i]*df_prices.loc[orders_df.index[i],orders_df.Symbol[i]]*(1-impact)-commission
    #print df_trades

    df_holdings=df_trades.copy()
    for i in range(0,len(df_holdings)):
        if i == 0:
            df_holdings.loc[df_holdings.index[i],'CASH']+=start_val
        else:
            df_holdings.loc[df_holdings.index[i],:]+=df_holdings.loc[df_holdings.index[i-1],:]
    #print df_holdings

    df_value=df_holdings.copy()

    for i in range(0,len(df_holdings)):
        for symbol in symbols:
            df_value.loc[df_holdings.index[i],symbol]=df_holdings.loc[df_holdings.index[i],symbol]*df_prices.loc[df_holdings.index[i],symbol]

    #print df_value

    #port_vals=[pd.DataFrame(0,index=dates)]
    port_vals=[]
    port_vals=pd.DataFrame(port_vals,index=index_dates)
    port_vals['VALUE']=0

    for i in range(0,len(df_value)):
        port_vals.ix[i]=df_value.ix[i,:].sum()

    #print port_vals
    last_day_portval=port_vals.ix[-1]

    num_days=len(port_vals)
    rfr=0
    daily_rets=port_vals.copy()
    daily_rets[1:]=(daily_rets[1:]/daily_rets[:-1].values)-1
    daily_rets=daily_rets[1:]
    #print daily_rets
    avg_daily_ret=daily_rets.mean()
    std_daily_ret=daily_rets.std()
    sharp_ratio=math.sqrt(num_days)*(np.mean(daily_rets-rfr)/daily_rets.std())

    #print num_days
    #print last_day_portval
    #print sharp_ratio
    #print avg_daily_ret

    return port_vals

def author():
    return 'cwu392'

def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/orders-02.csv"
    sv = 1000000

    # Process orders
    portvals = compute_portvals(orders_file = of, start_val = sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]] # just get the first column
    else:
        "warning, code did not return a DataFrame"
    
    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    start_date = dt.datetime(2008,1,1)
    end_date = dt.datetime(2008,6,1)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2,0.01,0.02,1.5]
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2,0.01,0.02,1.5]

    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of SPY : {}".format(cum_ret_SPY)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])

if __name__ == "__main__":
    #test_code()
    compute_portvals()
    #print marketsim.author