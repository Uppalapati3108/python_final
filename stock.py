# -*- coding: utf-8 -*-
"""
@author: kavya Uppalapati
"""

from datetime import date
#%%
class stock():
    def __init__(self, symbol, Open, high, low, close, volume):
        self.symbol = symbol
        self.Open = Open
        self.high = high
        self.close = close
        self.low = low
        self.volume = volume
        self.final_stock_price = []
        self.stock_date = []
        
    def final_stock(self, close, volume, date):
        final_price = close*volume
        self.final_stock_price.append(final_price)
        self.stock_date.append(date)

#%%
class Stock:
    def __init__(self, symbol, no_of_shares, purchase_price, current_price, date_purchased, purchase_id):
        self.symbol = symbol
        self.no_of_shares = no_of_shares
        self.purchase_price = purchase_price
        self.current_price = current_price
        self.date_purchased = date_purchased
        self.purchase_id = purchase_id
    
    def per_unit_stock_change(self):
        change = self.current_price - self.purchase_price
        return change
    
    def calc_loss_or_gain_amount(self):
        final_change = self.no_of_shares * self.per_unit_stock_change()
        return final_change
    
    def per_unit_percentage_change(self):
        percent_change = self.per_unit_stock_change()/self.purchase_price *100
        return percent_change
    
    def calc_percent_change_yearly(self):
        today = date.today()
        yearly_change = self.per_unit_percentage_change() / ((today - self.date_purchased).days/365)
        return yearly_change
    
    def get_stock_symbol(self):
        return self.symbol

    def get_num_shares(self):
        return self.no_of_shares

    def get_purchase_price(self):
        return self.purchase_price

    def get_current_price(self):
        return self.current_price

    def get_purchase_date(self):
        return self.date_purchased
        
class Bond(Stock):
    def __init__(self, symbol, no_of_shares, purchase_price, current_price, date_purchased, purchase_id, coupon, bond_yield):
        super().__init__(symbol, no_of_shares, purchase_price, current_price, date_purchased, purchase_id)
        self.coupon = coupon
        self.bond_yield = bond_yield

    def get_coupon(self):
        return self.coupon

    def get_bond_yield(self):
        return self.bond_yield

class Investor:
    def __init__(self, investor_id, address, phone_no):
        self.investor_id = investor_id
        self.address = address
        self.phone_no = phone_no
        self.stocks = []  
        self.bonds = []

    def add_stock(self, stock):
        self.stocks.append(stock)

    def add_bond(self, bond):
        self.bonds.append(bond)

    def get_stocks(self):
        return self.stocks[:]

    def get_bonds(self):
        return self.bonds[:]
