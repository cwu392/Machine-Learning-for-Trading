"""MC2-P1: Market simulator."""

import pandas as pd
import numpy as np
import datetime as dt
import os
import util as ut
import math
from indicators import indicators
import marketsim


def author():
    return 'cwu392'

def test_code(stock, start_date, end_date, sv):

    # benchmark, buy 1000 at JPM at initial date, sell them at ending date
    amount = 1000
    benchmark = ut.create_benchmark(stock[0], amount, sv, start_date, end_date)

    # run manual strategy
    of = "./orders/my_strategy.csv"
    
    # Process orders
    portvals = marketsim.compute_portvals(orders_file = of, start_val = sv)

    # print information

    ut.draw_charts([benchmark, portvals])



if __name__ == "__main__":
    #test_code(stock=['JPM'],  start_date='2008-1-1',end_date='2009-12-31',sv = 100000)
    test_code(stock=['JPM'],  start_date='2010-1-1',end_date='2011-12-31',sv = 100000)
    #compute_portvals()
    #print marketsim.author