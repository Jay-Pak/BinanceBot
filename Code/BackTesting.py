import pandas as pd
import numpy as np
import pprint

#RSI 계산
def RSI(data: pd.DataFrame, period : int = 14):
    delta = data['Close'].diff()
    ups, downs = delta.copy(), delta.copy()
    ups[ups < 0] = 0
    downs[downs > 0] = 0
    au = ups.ewm(com = period - 1, min_periods = period).mean()
    ad = downs.abs().ewm(com = period - 1, min_periods = period).mean()

    RS = au/ad
    RSI = pd.Series(100 - (100/(1+RS)), name='RSI')
    return RSI

#청산가 계산
maint_lookup_table = [
    (     50_000,  0.4,           0),
    (    250_000,  0.5,          50),
    (  1_000_000,  1.0,       1_300),
    ( 10_000_000,  2.5,      16_300),
    ( 20_000_000,  5.0,     266_300),
    ( 50_000_000, 10.0,   1_266_300),
    (100_000_000, 12.5,   2_516_300),
    (200_000_000, 15.0,   5_016_300),
    (300_000_000, 25.0,  25_016_300),
    (500_000_000, 50.0, 100_016_300),
]

def binance_btc_liq_balance(wallet_balance, contract_qty, entry_price):
    for max_position, maint_margin_rate_pct, maint_amount in maint_lookup_table:
        maint_margin_rate = maint_margin_rate_pct / 100
        liq_price = (wallet_balance + maint_amount - contract_qty*entry_price) / (abs(contract_qty) * (maint_margin_rate - (1 if contract_qty>=0 else -1)))
        base_balance = liq_price * abs(contract_qty)
        if base_balance <= max_position:
            break
    return abs(entry_price - round(liq_price, 2))

#수익금
def amount_of_profit_for_long(user_price, closed_price, margin, leverage):
    result = leverage * ((closed_price - user_price)/user_price) * margin
    return result

def amount_of_profit_for_short(user_price, closed_price, margin, leverage):
    result = leverage * ((user_price - closed_price)/user_price) * margin
    return result

#수익률
def profit_Rate(profit, margin):
    result = profit/margin * 100
    return result

#일봉 백테스팅
directory = 'Data/BTCUSDT_Binance_futures_UM_day.csv'
temp_btc1d = pd.read_csv(directory)
btc1d = temp_btc1d.loc[::-1].reset_index(drop=True)
btc1d['Date'] = pd.to_datetime(btc1d.Date)
btc1d.set_index('Date', inplace=True)

RSI = RSI(btc1d)

#BTC1D Call 방법 인덱스 : BTC1D.index[i], Close: BTC1D['Close'][i], RSI: BTC1D['RSI'][i]
BTC1D = pd.concat([btc1d['Close'], RSI], axis = 1)

leverage = 5
margin = 1000
total_balance = margin * leverage
betSize = total_balance/7
status = ''
user_price = 0
count = 0
pre_betSize = 0

total_profit = 0
win_rate = 0
win = 0
lose = 0
print('------------------------------------------------------------------------------------')

for i in range(len(BTC1D)):
    if(count == 0 and BTC1D['RSI'][i] <= 25):
        status = 'long'
        user_price = BTC1D['Close'][i]
        count += 1
        pre_betSize = betSize
        print('롱진입 성공!!! 롱 진입가 : ', user_price, 'count : ', ' closed_price : ',BTC1D['Close'][i], count, 'i : ', i, ' RSI : ',BTC1D['RSI'][i])
        continue
    elif(count == 0 and BTC1D['RSI'][i] >= 75):
        status = 'short'
        user_price = BTC1D['Close'][i]
        count += 1
        pre_betSize = betSize
        print('숏진입 성공!!! 숏 진입가 : ', user_price, 'count : ',' closed_price : ',BTC1D['Close'][i], count, 'i : ', i, ' RSI : ',BTC1D['RSI'][i])
        continue
    
#청산가 도달 시 청산
    if(status == 'long'):
        if(BTC1D['Close'][i] <= user_price - binance_btc_liq_balance(pre_betSize/leverage, pre_betSize/user_price, user_price)):
            print('롱으로 청산하셨습니다. ', 'user_price : ', user_price, 'liq_price : ', user_price - binance_btc_liq_balance(pre_betSize/leverage, pre_betSize/user_price, user_price), ' closed_price : ',BTC1D['Close'][i], ' RSI : ',BTC1D['RSI'][i])
            lose += 1
            status = ''
            user_price = 0
            pre_betSize = 0
            total_profit = -99999999999999999999999999999999999999
    elif(status == 'short'):
        if(BTC1D['Close'][i] >= user_price + binance_btc_liq_balance(pre_betSize/leverage, pre_betSize/user_price, user_price)):
            print('숏으로 청산하셨습니다. ', 'user_price : ', user_price, 'liq_price : ', user_price + binance_btc_liq_balance(pre_betSize/leverage, pre_betSize/user_price, user_price), ' closed_price : ',BTC1D['Close'][i], ' RSI : ',BTC1D['RSI'][i])
            lose += 1
            status = ''
            user_price = 0
            pre_betSize = 0
            total_profit = -99999999999999999999999999999999999999

    if(count >= 1 and count < 7 and status == 'long'):
        if(BTC1D['RSI'][i] <= 30):
            user_price = ((user_price*pre_betSize) + BTC1D['Close'][i]*(betSize))/(pre_betSize + betSize)
            pre_betSize += betSize
            print('롱 물타기 완료, 현재 평단 user_price : ', user_price, ' pre_betSize : ', pre_betSize, ' closed_price : ',BTC1D['Close'][i], ' RSI : ',BTC1D['RSI'][i])
    elif(count >=1 and count < 7 and status == 'short'):
        if(BTC1D['RSI'][i] >= 70):
            user_price = ((user_price*pre_betSize) + BTC1D['Close'][i]*(betSize))/(pre_betSize + betSize)
            pre_betSize += betSize
            print('숏 물타기 완료, 현재 평단 user_price : ', user_price, ' pre_betSize : ', pre_betSize, ' closed_price : ',BTC1D['Close'][i], ' RSI : ',BTC1D['RSI'][i])
#익절 손절(정한 수치 수익률에 따라)
    if(status == "long" and profit_Rate(amount_of_profit_for_long(user_price, BTC1D['Close'][i], pre_betSize/leverage, leverage), pre_betSize/leverage) >= 20):
        print('롱 익절 완료 user_price : ', user_price, ' closed_price : ', BTC1D['Close'][i], '수익금 : ', amount_of_profit_for_long(user_price, BTC1D['Close'][i], pre_betSize/leverage, leverage), ' 수익률 : ', profit_Rate(amount_of_profit_for_long(user_price, BTC1D['Close'][i], pre_betSize/leverage, leverage), pre_betSize/leverage))
        total_profit += amount_of_profit_for_long(user_price, BTC1D['Close'][i], pre_betSize/leverage, leverage)
        win += 1
        count = 0
        status = ""
        user_price = 0
        pre_betSize = 0
        continue
            
    elif(status == "long" and profit_Rate(amount_of_profit_for_long(user_price, BTC1D['Close'][i], pre_betSize/leverage, leverage), pre_betSize/leverage) <= -10):
        print('롱 손절 완료 user_price : ', user_price, ' closed_price : ', BTC1D['Close'][i], '수익금 : ', amount_of_profit_for_long(user_price, BTC1D['Close'][i], pre_betSize/leverage, leverage), ' 수익률 : ', profit_Rate(amount_of_profit_for_long(user_price, BTC1D['Close'][i], pre_betSize/leverage, leverage), pre_betSize/leverage))
        total_profit += amount_of_profit_for_long(user_price, BTC1D['Close'][i], pre_betSize/leverage, leverage)
        lose += 1
        count = 0
        status = ""
        user_price = 0
        pre_betSize = 0
        continue
        
    elif(status == "short" and profit_Rate(amount_of_profit_for_short(user_price, BTC1D['Close'][i], pre_betSize/leverage, leverage), pre_betSize/leverage) >= 20):
        print('숏 익절 완료 user_price : ', user_price, ' closed_price : ', BTC1D['Close'][i], '수익금 : ', amount_of_profit_for_short(user_price, BTC1D['Close'][i], pre_betSize/leverage, leverage), ' 수익률 : ', profit_Rate(amount_of_profit_for_short(user_price, BTC1D['Close'][i], pre_betSize/leverage, leverage), pre_betSize/leverage))
        total_profit += amount_of_profit_for_short(user_price, BTC1D['Close'][i], pre_betSize/leverage, leverage)
        win += 1
        count = 0
        status = ""
        user_price = 0
        pre_betSize = 0
        continue
        
    elif(status == "short" and profit_Rate(amount_of_profit_for_short(user_price, BTC1D['Close'][i], pre_betSize/leverage, leverage), pre_betSize/leverage) <= -10):
        print('숏 손절 완료 user_price : ', user_price, ' closed_price : ', BTC1D['Close'][i], '수익금 : ', amount_of_profit_for_short(user_price, BTC1D['Close'][i], pre_betSize/leverage, leverage), ' 수익률 : ', profit_Rate(amount_of_profit_for_short(user_price, BTC1D['Close'][i], pre_betSize/leverage, leverage), pre_betSize/leverage))
        total_profit += amount_of_profit_for_short(user_price, BTC1D['Close'][i], pre_betSize/leverage, leverage)
        lose += 1
        count = 0
        status = ""
        user_price = 0
        pre_betSize = 0
        continue
    
#7일간 매수 후  7일이 지났으면 손절 or 익절
    if(count >= 13 and status == 'long'):
        if(amount_of_profit_for_long(user_price, BTC1D['Close'][i], pre_betSize/leverage, leverage) >= 0):
            win += 1
            total_profit += amount_of_profit_for_long(user_price, BTC1D['Close'][i], pre_betSize/leverage, leverage)
            print('7일 지나서 롱 익절 완료 user_price : ', user_price, ' pre_betSize : ', pre_betSize, '수익금', amount_of_profit_for_long(user_price, BTC1D['Close'][i], pre_betSize/leverage, leverage), ' closed_price : ',BTC1D['Close'][i],)
        else:
            lose += 1
            total_profit += amount_of_profit_for_long(user_price, BTC1D['Close'][i], pre_betSize/leverage, leverage)
            print('7일 지나서 롱 손절 완료 user_price : ', user_price, ' pre_betSize : ', pre_betSize, '수익금', amount_of_profit_for_long(user_price, BTC1D['Close'][i], pre_betSize/leverage, leverage), ' closed_price : ',BTC1D['Close'][i],)
        count = 0
        status = ""
        user_price = 0
        pre_betSize = 0
    elif(count >= 13 and status == 'short'):
        if(amount_of_profit_for_short(user_price, BTC1D['Close'][i], pre_betSize/leverage, leverage) >= 0):
            win += 1
            total_profit += amount_of_profit_for_short(user_price, BTC1D['Close'][i], pre_betSize/leverage, leverage)
            print('7일 지나서 숏 익절 완료 user_price : ', user_price, ' pre_betSize : ', pre_betSize, '수익금', amount_of_profit_for_short(user_price, BTC1D['Close'][i], pre_betSize/leverage, leverage), ' closed_price : ',BTC1D['Close'][i],)
        else:
            lose += 1
            total_profit += amount_of_profit_for_short(user_price, BTC1D['Close'][i], pre_betSize/leverage, leverage)
            print('7일 지나서 숏 손절 완료 user_price : ', user_price, ' pre_betSize : ', pre_betSize, '수익금', amount_of_profit_for_short(user_price, BTC1D['Close'][i], pre_betSize/leverage, leverage), ' closed_price : ',BTC1D['Close'][i],)
        count = 0
        status = ""
        user_price = 0
        pre_betSize = 0

    if(count >= 1):
        count +=1

print(total_profit, win, lose)