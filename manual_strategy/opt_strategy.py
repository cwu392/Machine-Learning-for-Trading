
import pandas as pd
import util as ut
import datetime as dt
import marketsim
import numpy as np


def determine_optimal_orders(stock, start_date, end_date):

    # Get price data
    dates = pd.date_range(start_date, end_date)
    prices_all = ut.get_data(stock, dates)  # Adds SPY
    prices = prices_all[stock]  # Remove SPY

    # If we can see the future: the best strategy is buy while it's rising
    # and sell while its falling
    daily_rets = prices.diff(periods=1).shift(-1)
    position = np.sign(daily_rets) * 1000
    position.ix[-1, :] = 0  # Sell Everything On Last Day

    # Calculate Optimal Orders
    orders = pd.DataFrame(0, index=position.index, columns=stock)
    orders = position.diff(1)
    orders.ix[0, :] = position.ix[0, :]  # fix initial day position

    return orders


def create_optimal_portfolio(stock, sv, start_date, end_date):

    orders = determine_optimal_orders(stock=stock,start_date=start_date,end_date=end_date)
    optimal_orders = './orders/optimal_orders.csv'
    ut.write_orders_to_csv(orders, optimal_orders)

    # Calculate portfolio:
    optimal_portfolio = marketsim.compute_portvals(orders_file=optimal_orders,start_val=sv)
    optimal_portfolio = optimal_portfolio[optimal_portfolio.columns[0]]

    return optimal_portfolio


def test_code(stock, start_date, end_date, sv, draw_charts=False):

    amount = 1000
    benchmark = ut.create_benchmark(stock[0], amount, sv, start_date, end_date)
    optimal_portfolio = create_optimal_portfolio(stock, sv,start_date, end_date)

    # Plot
    if draw_charts==True:
        ut.draw_charts([benchmark, optimal_portfolio])


if __name__ == '__main__':
    stock = ['JPM']
    sv = 100000

    start_date = dt.datetime(2008, 1, 1)
    end_date = dt.datetime(2009, 12, 31)
    test_code(stock, start_date, end_date, sv, draw_charts=True)

#    start_date = dt.datetime(2010, 1, 1)
#    end_date = dt.datetime(2011, 12, 31)
#    test_code(stock, start_date, end_date, sv, draw_charts=True)