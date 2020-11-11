# -*- coding: utf-8 -*-
import baostock as bs
import sys
from util import *
from indicator import *
import pandas as pd
import matplotlib.pyplot as plt
import pdb

index_pro="date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST"
index_mini="date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg"

class bsAgent:
    @property
    def freq(self):
        return self._freq
    @property
    def k_data(self):
        return self._k_data
    @property
    def k_data_plus(self):
        return self._k_data_plus
    @property
    def kdj(self):
        return self._kdj
    @property
    def macd(self):
        return self._macd

    def login(self):
        res = bs.login(user_id="anonymous", password="123456")
        show_error(sys._getframe().f_code.co_name, res)
    def load_his_k_data(self, stack_code, start_date, end_date):
        #### 获取历史K线数据 ####
        data_list = []
        res = bs.query_history_k_data(stack_code,index_pro if self._freq=='d' else index_mini,
            start_date=start_date, end_date=end_date, 
            frequency=self._freq, adjustflag="3") #frequency="d"取日k线，adjustflag="3"默认不复权
        show_error(sys._getframe().f_code.co_name, res)
        while (res.error_code == '0') & res.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(res.get_row_data())
        df_data = pd.DataFrame(data_list, columns=res.fields)
        df_data.set_index(["date"], inplace=True)
        df_data[['low','high','close']] = df_data[['low','high','close']].astype(float)
        self._k_data = df_data
        self._k_data_plus = df_data
    def trade(self, trade, price):
        return -trade*price if trade==trade else 0
    def plot(self, indicator):
        if indicator is Indicator.KDJ_X:
            self.k_data_plus[['close']].plot(title='close',figsize=(30, 6.5))
            self.k_data_plus[['K','D','J']].plot(title='KDJ',figsize=(30, 6.5))
            self.k_data_plus[['assets']].plot(title='assets',figsize=(30, 6.5))
        if indicator is Indicator.MACD_X:
            self.k_data_plus[['close']].plot(title='close',figsize=(30, 6.5))
            ax = self.k_data_plus[['dif','dea','hist']].plot(title='MACD',figsize=(30, 6.5))
            ax.axhline(y=0)
            self.k_data_plus[['assets']].plot(title='assets',figsize=(30, 6.5))
        plt.show()
    def replay(self, indicator, start_date, end_date, view='false'):
        if indicator is Indicator.KDJ_X:
            self._kdj = compute_kdj(self.k_data)
            self._k_data_plus = self.k_data_plus.join(self.kdj,how='left',lsuffix='_left',rsuffix='_right')
        if indicator is Indicator.MACD_X:
            self._macd = compute_macd(self.k_data)
            self._k_data_plus = self.k_data_plus.join(self.macd,how='left',lsuffix='_left',rsuffix='_right')
        # pdb.set_trace()
        self.k_data_plus['crash'] = self.k_data_plus[(self.k_data_plus.index>start_date) & (self.k_data_plus.index<end_date)].apply(lambda row: self.trade(row[indicator.value],row['close']), axis=1).cumsum()
        self.k_data_plus['share'] = self.k_data_plus[(self.k_data_plus.index>start_date) & (self.k_data_plus.index<end_date)][indicator.value].cumsum()*self.k_data_plus.close
        self.k_data_plus['assets'] = self.k_data_plus['crash'] + self.k_data_plus['share']
        if view:
            self.plot(indicator)
    
    def __init__(self, stack_code='000016.sh',start_date='2020-04-01', end_date='2020-10-13', freq='d'):
        self._freq = freq
        self.login()
        self.load_his_k_data(stack_code, start_date, end_date)
