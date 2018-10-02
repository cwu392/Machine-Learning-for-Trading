import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data
import math
from marketsim import compute_portvals
from itertools import tee, izip
from datetime import timedelta
import matplotlib.pyplot as plt

def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

def indicators(prices_all,dates,stock):
	# Calculate Bollinger Bands (R) for our stock
	bollinger_pd=pd.DataFrame(index=dates)
	bollinger_pd[stock]=prices_all[stock]/prices_all[stock][0]
	bollinger_pd.dropna(inplace=True)
	bollinger_pd[stock]=bollinger_pd[stock]/bollinger_pd[stock][0]
	bollinger_pd['rolling_mean']=pd.rolling_mean(prices_all[stock]/prices_all[stock][0],window=20)
	#bollinger_pd['rolling_mean'].fillna(method='backfill')
	rolling_std=pd.rolling_std(prices_all[stock]/prices_all[stock][0],window=20)
	#rolling_std.fillna(method='backfill')
	bollinger_pd['upper_bound']=bollinger_pd['rolling_mean']+(2.0*rolling_std)
	bollinger_pd['lower_bound']=bollinger_pd['rolling_mean']-(2.0*rolling_std)

	# bollinger_pd has columns date, JPM, rolling_mean, upper_bound, lower_bound
	# First 20 rows(window size) are NaN

	# My Strategy:
	## 1. If Stock cross Bollinger Band
	## 2. If SPY up/down
	## 3. If 1-day Momentum up/down

	# Initialization:
	Long_Stock=[]
	Short_Stock=[]
	Exit_Stock=[]
	Current_Long="0"
	Current_Short="0"
	f=open('./orders/my_strategy.csv','w')
	f.write("Date,Symbol,Order,Shares\n") # create the same file for marketsim.py

	# Start Manual Strategy:
	for (index1,value1),(index2,value2) in pairwise(bollinger_pd.iterrows()):
		# From Hint 1: bb_value[t] = (price[t] - SMA[t])/(2 * stdev[t])

		#Initialize Momentum:
		## Calculate 1-Day Momentum:
		momentum=0.0
		if ((index2-timedelta(days=3)) in bollinger_pd.index):
			momentum=(bollinger_pd.loc[index2,stock]/bollinger_pd.loc[index2-timedelta(days=3),stock])-1.0

		# My Strategy:
		## 1. When should you buy: BB, Momentum, SMA:
		if (value1[stock]<value1['lower_bound'] and value2[stock]>value2['lower_bound']) or (momentum>0.25) and (Current_Long=='F' or '0'):
			Long_Stock.append(str(index2))
			Current_Long="T"
			f.write("{},{},BUY,300\n".format(str(index2),stock))
		## 2. When should you sell: BB, SMA:
		elif (value1[stock]>value1['rolling_mean'] and value2[stock]>value2['rolling_mean']) and (Current_Long=='T'):
			Exit_Stock.append(str(index2))
			Current_Long='F'
			f.write("{},{},SELL,300\n".format(str(index2),stock))
		## 3. When should you short: BB, Momentum, SMA:
		elif (value1[stock]>value1['upper_bound'] and value2[stock]<value2['upper_bound']) or (momentum<-0.25) and (Current_Short=='F' or '0'):			
			Short_Stock.append(str(index2))
			Current_Short='T'
			f.write("{},{},SELL,300\n".format(str(index2),stock))
		## 4. When should you stop shorting: BB, Momentum, SMA:	
		elif (value1[stock]>value1['rolling_mean'] and value2[stock]<value2['rolling_mean']) and (Current_Short=='T'):
			Exit_Stock.append(str(index2))
			Current_Short='F'
			f.write("{},{},BUY,300\n".format(str(index2),stock))
	f.close()

	# Create BB Plot:
	figure=bollinger_pd.plot(fontsize=12)
	figure.set_xlabel("Date")
	figure.set_ylabel("Prices") 
	for index,value in enumerate(Long_Stock):
		figure.axvline(x=value,ymin=0,ymax=100,linewidth=0.5,color='green')
	for index,value in enumerate(Short_Stock):
		figure.axvline(x=value,ymin=0,ymax=100,linewidth=0.5,color='red')
	plt.show()

	# Create SMA Plot:
	# sma_pd=pd.DataFrame(index=dates)
	# sma_pd[stock]=prices_all[stock]/prices_all[stock][0]
	# sma_pd.dropna(inplace=True)
	# sma_pd[stock]=sma_pd[stock]/sma_pd[stock][0]
	# sma_pd['SMA window=5']=pd.rolling_mean(prices_all[stock]/prices_all[stock][0],window=5)
	# sma_pd['SMA window=10']=pd.rolling_mean(prices_all[stock]/prices_all[stock][0],window=10)
	# sma_pd['SMA window=20']=pd.rolling_mean(prices_all[stock]/prices_all[stock][0],window=20)
	# figure=sma_pd.plot(fontsize=12)
	# figure.set_xlabel("Date")
	# figure.set_ylabel("Prices") 
	# plt.show()

def run():
	#Training
	start_date='2008-1-1'
	end_date='2009-12-31'

	#Testing
	# start_date='2010-1-1'
	# end_date='2011-12-31'

	stock='JPM'

	dates=pd.date_range(start_date,end_date)
	prices_all=get_data([stock],dates)

	indicators(prices_all,dates,stock)
	compute_portvals("./orders/my_strategy.csv",prices_all,dates,stock)

if __name__ == "__main__":
	run()