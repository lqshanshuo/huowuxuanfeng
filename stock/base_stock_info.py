# -*- coding:utf-8 -*-
import baostock as bs
import sys
import pandas as pd

print("be happy!")

class BaseStockInfo(object):

    def __init__(self, stock_code, start_date, end_date, freq="d"):
        self._freq = freq
        self._k_data = None
        self._k_data_plus = None
        self._stock_code = stock_code
        self._start_date = start_date
        self._end_date = end_date

    def __str__(self):
        return str(self._k_data)






