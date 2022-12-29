import time
import datetime
import pandas as pd
import numpy as np

directory = 'Data\gemini_BTCUSD_d.csv'
btc1d = pd.read_csv(directory)

# print(btc1d['close'])

def RSI(df, period):
    U = np.where(df.diff(1)['close'] > 0, df.diff(1)['close'], 0)
    D = np.where(df.diff(1)['close'] < 0, df.diff(1)['close'] * (-1), 0)
    AU = pd.DataFrame(U, index=date_index)