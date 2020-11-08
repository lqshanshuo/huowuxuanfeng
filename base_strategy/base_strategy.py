# -*- coding:utf-8 -*-

print("make more money!\nbe happy!")


class BaseStrategy(object):

    def __init__(self):
        pass

    '''
    每天交易时
    '''
    def handle_data(context, data):
        if g.if_trade == True:
            # 计算现在的总资产，以分配资金，这里是等额权重分配
            g.everyStock = context.portfolio.portfolio_value / g.N
            # 获得今天日期的字符串
            todayStr = str(context.current_dt)[0:10]
            # 获得因子排序
            a, b = getRankedFactors(g.factors, todayStr)
            # 计算每个股票的得分
            points = np.dot(a, g.weights)
            # 复制股票代码
            stock_sort = b[:]
            # 对股票的得分进行排名
            points, stock_sort = bubble(points, stock_sort)
            # 取前N名的股票
            toBuy = stock_sort[0:g.N].values
            # 对于不需要持仓的股票，全仓卖出
            order_stock_sell(context, data, toBuy)
            # 对于不需要持仓的股票，按分配到的份额买入
            order_stock_buy(context, data, toBuy)
        g.if_trade = False

    '''
    每天收盘后
    '''

    # 每日收盘后要做的事情（本策略中不需要）
    def after_trading_end(context):
        return
