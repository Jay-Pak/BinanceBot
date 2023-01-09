user_price = 1000
pre_betSize = 2000

current_price = 2000
betSize = 1000

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

# print(profit_Rate(amount_of_profit_for_long(1000, 2000, 1000, 5), 1000))




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
    return round(liq_price, 2)

leverage = 5
margin = 1000
total_balance = margin * leverage
betSize = total_balance/7
status = ''
user_price = 10000
user_liq_price = 0
count = 0
pre_betSize = betSize

print(binance_btc_liq_balance(pre_betSize/leverage, pre_betSize/user_price, user_price))