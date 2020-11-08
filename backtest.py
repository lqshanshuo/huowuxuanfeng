# -*- coding:utf-8 _*-
from daily_run.dailyrun import DailyRun

print("be happy!")

stock_path = "../resource/target_stock.dat"
account_dir = "../resource/user_account"
start_date = "2020-04-01"
end_date = "2020-10-01"


mode = "backtest" # backtest or dailyrun

# 初始化股票信息
DR = DailyRun(stock_path, account_dir, start_date, end_date)

# 计算某一天的交易建议，默认使用此天以前的数据，不包含当天。
tra_result = DR.trade_reference_answer()

# 立即执行交易建议
DR.backtest_do_trade(tra_result)

# 计算账户最新状态
DR.update_user_account()

# 根据T日收盘价计算近似收益(假设随时能够买卖)
DR.cal_gain()

# 保存当天交易状态。等待下次启动。
DR.close()
