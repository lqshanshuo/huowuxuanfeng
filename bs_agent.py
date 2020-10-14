import baostock as bs
import pandas as pd
class bsAgent:
    @property
    def k_data(self):
        return self._k_data
    @property
    def k_data_plus(self):
        return self._k_data_plus
    @property
    def kdj(self):
        return self._kdj

    def login(self):
        lg = bs.login(user_id="anonymous", password="123456")
        print('login respond error_code:'+lg.error_code)
        print('login respond  error_msg:'+lg.error_msg)
    def load_his_k_data(self, stack_code, start_date, end_date):
        #### 获取历史K线数据 ####
        data_list = []
        rs = bs.query_history_k_data(stack_code,
            "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST",
            start_date=start_date, end_date=end_date, 
            frequency="d", adjustflag="3") #frequency="d"取日k线，adjustflag="3"默认不复权
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())
        df_data = pd.DataFrame(data_list, columns=rs.fields)
        df_data.set_index(["date"], inplace=True)
        df_data[['low','high','close']] = df_data[['low','high','close']].astype(float)
        self._k_data = df_data
    def compute_kdj(self):
        # 剔除停盘数据
        df_init = self.k_data
        df_status = df_init[df_init['tradestatus'] == '1']
        # 计算KDJ指标,前9个数据为空
        low_list = df_status['low'].rolling(window=9).min()
        high_list = df_status['high'].rolling(window=9).max()
        rsv = (df_status['close'] -low_list) / (high_list -low_list) * 100
        df_data = pd.DataFrame()
        df_data['K'] = rsv.ewm(com=2).mean()
        df_data['D'] = df_data['K'].ewm(com=2).mean()
        df_data['J'] = 3* df_data['K'] -2* df_data['D']
        df_data.index = df_status.index.values
        df_data.index.name = 'date'
        # 删除空数据
        df_data = df_data.dropna()
        # 计算KDJ指标金叉、死叉情况
        df_data['KDJ_x'] = 0
        kdj_position = df_data['K'] > df_data['D']
        df_data.loc[kdj_position[(kdj_position == True) & (kdj_position.shift() == False)].index, 'KDJ_x'] = 1
        df_data.loc[kdj_position[(kdj_position == False) & (kdj_position.shift() == True)].index, 'KDJ_x'] = -1
        # df_data.plot(title='KDJ',figsize=(30, 6.5))
        # plt.show()
        self._kdj = df_data
        self._k_data_plus = self.k_data.join(self.kdj,how='left',lsuffix='_left',rsuffix='_right')
    def trade(self, trade, price):
        return -trade*price if trade==trade else 0
    def simulation(self, signal_col):
        self.k_data_plus['crash'] = self.k_data_plus.apply(lambda row: self.trade(row[signal_col],row['close']), axis=1).cumsum()
        self.k_data_plus['share'] = self.k_data_plus[signal_col].cumsum()*self.k_data_plus.close
        self.k_data_plus['assets'] = self.k_data_plus['crash'] + self.k_data_plus['share']
    
    def __init__(self, stack_code='000016.sh',start_date='2020-04-01', end_date='2020-10-13'):
        self.login()
        self.load_his_k_data(stack_code, start_date, end_date)
