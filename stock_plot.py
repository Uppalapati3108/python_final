# -*- coding: utf-8 -*-
"""
@author: Kavya Uppalapati
"""

from stock import stock, Stock, Bond, Investor
import json
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import seaborn as sns
import mplfinance as mpf
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpdates
from yahoo_finance import Share
import yfinance as yf
import numpy as np
from datetime import date
#%%
data_file = "AllStocks (4).json"
try:
    with open(data_file, 'r') as f:
        data_set = json.load(f)
except Exception as e:
    print(e)
#%%
stockdictionary = {}

for stock_item in data_set:
    if stock_item['Symbol'] not in stockdictionary:
        new_stock = stock(stock_item['Symbol'], stock_item['Open'], stock_item['High'], 
                          stock_item['Low'], stock_item['Close'], stock_item['Volume'])
        stockdictionary[stock_item['Symbol']] = new_stock
    
    stockdictionary[stock_item['Symbol']].final_stock(stock_item['Close'],stock_item['Volume'],
                                                     datetime.strptime(stock_item['Date'], '%d-%b-%y'))
#%%
for key, stock_items in stockdictionary.items():
    print (stock_items.symbol , stock_items.final_stock_price)
#%%
for stock_items in stockdictionary:
    final_stock_prices = stockdictionary[stock_items].final_stock_price
    final_dates = matplotlib.dates.date2num(stockdictionary[stock_items].stock_date)
    name = stockdictionary[stock_items].symbol
    plt.plot_date(final_dates, final_stock_prices, linestyle='solid',marker = 'None',label = name)

plt.legend()
plt.show()
#%%
df = pd.DataFrame(data_set) # we are creating a dataframe from the read json file data
# Converting the date column into datatime format by inferring the schema instead of defining the schema
df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True) 
# Now we will create the final stock price at each date end, by multiplying the close price with volume
df['Stock_price'] = df['Volume']*df['Close']
#%%
# Using seaborn package to plot the same information which we plotted using matplotlib
# In this we define x, y axes and then tell what the data is and also incorporate another column to distinguish category using Hue (color)
sns.catplot(x='Date', y='Stock_price', hue = 'Symbol', data=df, kind = 'point')
sns.catplot(x='Date', y='Stock_price', hue = 'Symbol', data=df, kind = 'bar')
#%%
'''
There are sone values which are having the value '-' in it. So we are identifying such and replacing
them with mean of the above and below value after sorting them based on date.
First we replace those values with nan using the help of numpy package
'''
df.replace('-',np.nan, inplace=True)

for label in list(df['Symbol'].unique()):
    df1 = df[df['Symbol']==label]
    df1.reset_index(inplace=True, drop=True)
    
    for col in df1.columns:
        na_index_list = df1[df1[col].isnull()].index.tolist()
        for j in na_index_list:
            df1[col][j] = (float(df1[col][j+1]) + float(df1[col][j-1]))/2 
    
    df1.set_index('Date', inplace=True)
    '''
    df1['Open'] = df1['Open'].astype(float)
    df1['High'] = df1['High'].astype(float)
    df1['Close'] = df1['Close'].astype(float)
    df1['Low'] = df1['Low'].astype(float)
    
    Instead of hard column each column to type float, a try except block trying to convert 
    every column to float is shown below
    '''
    for column in df1.columns:
        try:
            df1[column] = df1[column].astype(float)
        except:
            pass
    
    mpf.plot(df1,volume=True, show_nontrading=True, type='candle', title=label)
#%%
data = yf.download(tickers='AIG', period='6mo', interval = '15d')    
#%%
df = pd.read_csv('bob_shares.csv')
symbols = df['Stock Symbol'].to_list()
no_of_shares = df['No.Shares'].to_list()
purchase_prices = df['Purchase Price'].to_list()
current_prices = df['Current Value'].to_list()
#%%
bob = Investor(0, "123 Main St.", "+15055551212")
next_purchase_id = 0
next_investor_id = 1
#%%
for i in range(len(df)):
    bob.add_stock(Stock(symbols[i], no_of_shares[i], purchase_prices[i], current_prices[i], date(2017, 8, 1), next_purchase_id))
    next_purchase_id = next_purchase_id + 1

bob.add_stock(Stock("M", 425, 30.30, 23.98, date(2018, 1, 10), next_purchase_id))
next_purchase_id += 1
bob.add_stock(Stock("F", 85, 12.58, 10.95, date(2018, 2, 17), next_purchase_id))
next_purchase_id += 1
bob.add_stock(Stock("IBM", 80, 150.37, 145.30, date(2018, 5, 12), next_purchase_id))
bob.add_bond(Bond("GT2:GOV", 200, 100.02, 100.05, date(2017, 8, 1), 1.38, 1.35, next_purchase_id))
#%%
df_stock = pd.DataFrame(columns = list(df.columns))
df_stock['Purchase Date'] = ''
for stk in bob.get_stocks():
    df_stock = df_stock.append({'Stock Symbol':stk.get_stock_symbol(),'No.Shares':stk.get_num_shares(),
                     'Purchase Price':stk.get_purchase_price(), 'Current Value':stk.get_current_price(),
                     'Purchase Date':stk.get_purchase_date()}, ignore_index=True)
#%%
df_bond = pd.DataFrame(columns = list(df_stock.columns))
df_bond['Coupon'] = ''
df_bond['Yield'] = ''
for bond in bob.get_bonds():
    df_bond = df_bond.append({'Stock Symbol':bond.get_stock_symbol(),'No.Shares':bond.get_num_shares(),
                     'Purchase Price':bond.get_purchase_price(), 'Current Value':bond.get_current_price(),
                     'Purchase Date':bond.get_purchase_date(),'Coupon':bond.get_coupon(),
                     'Yield':bond.get_bond_yield()}, ignore_index=True)
#%%
value_change_list_stock = [stock.calc_loss_or_gain_amount() for stock in bob.get_stocks()]
yearly_earning_loss_stock = [stock.calc_percent_change_yearly() for stock in bob.get_stocks()]
df_stock['Earnings/Loss'] = value_change_list_stock
df_stock['Yearly Earnings/Loss'] = yearly_earning_loss_stock
#%%
value_change_bond = [stock.calc_loss_or_gain_amount() for stock in bob.get_bonds()]
yearly_change_bond = [stock.calc_percent_change_yearly() for stock in bob.get_bonds()]
df_bond['Earnings/Loss'] = value_change_bond
df_bond['Yearly Earnings/Loss'] = yearly_change_bond
