# -*- coding:utf-8 -*-
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from stock.base_stock_info import BaseStockInfo
from stock.stock_info_source import StockInfoSource
from daily_run.user_account import UserAccount

print("be happy!")


class DailyRun(object):

    def __init__(self, stock_path, account_dir, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

        self.target_stocks_list = []
        self.target_stock_infos = []

        self.read_target_stocks_list(stock_path)
        self.read_target_stock_infos()

        self.user_account = UserAccount(account_dir)

    def read_target_stocks_list(self, path):
        with open(path, "r") as finput:
            for line in finput:
                if '#' not in line:
                    line = line.strip().split(",")
                    self.target_stocks_list.append([line[0]])

    def read_target_stock_infos(self):
        assert(self.target_stocks_list is not None and len(self.target_stocks_list) >= 1)

        stock_info_source = StockInfoSource()
        for stock in self.target_stocks_list:
            stock_code = stock[0]
            bs = BaseStockInfo(stock_code, self.start_date, self.end_date)
            stock_info_source.load_his_k_data(bs)
            self.target_stock_infos.append(bs)

    def trade_reference_answer(self):
        pass

    def backtest_do_trade(self):
        pass

    def update_user_account(self):
        pass

    def cal_gain(self):
        pass








stock_path = "../resource/target_stock.dat"
account_dir = "../resource/user_account"
start_date = "2020-04-01"
end_date = "2020-10-01"
mode = "backtest" # backtest or dailyrun

# 初始化股票信息
DR = DailyRun(stock_path, account_dir, start_date, end_date)

# 计算某一天的交易建议
DR.trade_reference_answer()

# 立即执行交易建议
DR.backtest_do_trade()
# 计算账户最新状态
DR.update_user_account()
# 根据T日收盘价计算近似收益(假设随时能够买卖)
DR.cal_gain()
# 保存当天交易状态。等待下次启动。
DR.close()
