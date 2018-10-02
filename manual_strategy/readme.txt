Read Me:
Q1: Indicators
All codes including BB, Momentum and price/SMA are wrote in indicator.py
Figures are from run(), you can mark time range to get in/out of sample figures.
EX:
	#Training
	start_date='2008-1-1'
	end_date='2009-12-31'

	#Testing
	# start_date='2010-1-1'
	# end_date='2011-12-31'

Q2: Best Possible Strategy:
Code to find optimum are wrote in this way.
1. looking for all rising points
2. buy
Code are in opt_strategy.py
plots should use util.py->draw_charts
as Q1, you can still choose different st,ed to get figures.
EX:

    start_date = dt.datetime(2008, 1, 1)
    end_date = dt.datetime(2009, 12, 31)
    test_code(stock, start_date, end_date, sv, draw_charts=True)

#    start_date = dt.datetime(2010, 1, 1)
#    end_date = dt.datetime(2011, 12, 31)
#    test_code(stock, start_date, end_date, sv, draw_charts=True)

Q3: Manual Rule-Based Trader:
Code are also in indicator.py
I use f.write, in this case, Please Create A Folder Named 'order' Before Running~!!!!
my indicator.py will generate a file the same as provided.
This is to avoid rewrite marketsim.py~!!!!

Q4: Manual vs Benchmark:
These figures can be generate by marketsim_2.py
I am sorry about the naming, but my mouse is broken, I temporarily can't change my file name.
In this python file, you can still change the time span to get both plots.