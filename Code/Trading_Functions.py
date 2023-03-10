import pandas as pd

# directory = 'Data\gemini_BTCUSD_d.csv'
# btc1d = pd.read_csv(directory)
# r_idx = [i for i in range(btc1d.shape[0]-1,-1,-1)]
# r_btc1d = pd.DataFrame(btc1d, index=r_idx)
# r_btc1d_close = r_btc1d['close']
# delta = r_btc1d_close.diff()
# ups, downs = delta.copy(), delta.copy()
# ups[ups < 0] = 0
# downs[downs > 0] = 0
# period = 14

# au = ups.ewm(com = period - 1, min_periods = period).mean()
# ad = downs.abs().ewm(com = period - 1, min_periods = period).mean()

# RS = au/ad
# RSI = pd.Series(100 - (100/(1+RS)))

# def reverse_data(data: pd.DataFrame):
#     r_idx = [i for i in range(data.shape[0]-1,-1,-1)]
#     r_data = pd.DataFrame(data, index = r_idx)


def RSI(data: pd.DataFrame, period : int = 14):
    delta = data['close'].diff()
    ups, downs = delta.copy(), delta.copy()
    ups[ups < 0] = 0
    downs[downs > 0] = 0
    au = ups.ewm(com = period - 1, min_periods = period).mean()
    ad = downs.abs().ewm(com = period - 1, min_periods = period).mean()

    RS = au/ad
    RSI = pd.Series(100 - (100/(1+RS)))
    return RSI
