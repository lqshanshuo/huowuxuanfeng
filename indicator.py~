from enum import Enum
import talib as ta
import pandas as pd

class Indicator(Enum):
    KDJ_X = 'kdj_x'
    MACD_X = 'macd_x'

def compute_macd(df):
    # 剔除停盘数据
    df_init = df[df['tradestatus'] == '1'] if 'tradestatus' in df.columns else df
    # 获取dif,dea,hist，它们的数据类似是tuple，且跟df_init的date日期一一对应
    # 记住了dif,dea,hist前33个为Nan，所以推荐用于计算的数据量一般为你所求日期之间数据量的3倍
    # 这里计算的hist就是dif-dea,而很多证券商计算的MACD=hist*2=(dif-dea)*2
    dif, dea, hist = ta.MACD(df_init['close'].astype(float).values, fastperiod=12, slowperiod=26, signalperiod=9)
    df_out = pd.DataFrame({'dif': dif[33:], 'dea': dea[33:], 'hist': hist[33:]},index=df_init.index.values[33:], columns=['dif', 'dea', 'hist'])
    # 计算MACD指标金叉和死叉
    df_out[Indicator.MACD_X.value] = 0
    macd_position = df_out['dif'] >= df_out['dea']
    df_out.loc[macd_position[(macd_position == True) & (macd_position.shift() == False)].index, Indicator.MACD_X.value] = 1
    df_out.loc[macd_position[(macd_position == False) & (macd_position.shift() == True)].index, Indicator.MACD_X.value] = -1
    return df_out

def compute_kdj(df):
    # 剔除停盘数据
    df_init = df[df['tradestatus'] == '1'] if 'tradestatus' in df.columns else df
    # 计算KDJ指标,前9个数据为空
    low_list = df_init['low'].rolling(window=9).min()
    high_list = df_init['high'].rolling(window=9).max()
    rsv = (df_init['close'] -low_list) / (high_list -low_list) * 100
    df_out = pd.DataFrame()
    df_out['K'] = rsv.ewm(com=2).mean()
    df_out['D'] = df_out['K'].ewm(com=2).mean()
    df_out['J'] = 3* df_out['K'] -2* df_out['D']
    df_out.index = df_init.index.values
    df_out.index.name = 'date'
    # 删除空数据
    df_out = df_out.dropna()
    # 计算KDJ指标金叉、死叉情况
    df_out[Indicator.KDJ_X.value] = 0
    kdj_position = df_out['K'] > df_out['D']
    df_out.loc[kdj_position[(kdj_position == True) & (kdj_position.shift() == False)].index, Indicator.KDJ_X.value] = 1
    df_out.loc[kdj_position[(kdj_position == False) & (kdj_position.shift() == True)].index, Indicator.KDJ_X.value] = -1
    return df_out
