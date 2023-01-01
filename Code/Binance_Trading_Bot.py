import pandas as pd
import numpy as np
import ccxt
import pprint


binance = ccxt.binance(config={
    'apiKey': 'Cwe4FBXBKX2mVxyq75oa8ItF9vO8nezS3jZkrGvAsBH2lVllQxv4fieAL0YZ20Nt',
    'secret': '0sCXhA8gUoLxKCimgyReRBTrJ5Bu10tDylPHXgVXff2CK0BL1LgLfOR4MnmwJafO',
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future'
    }
})

#레버리지 설정
markets = binance.load_markets()
symbol = "BTC/USDT"
market = binance.market(symbol)
leverage = 5

resp = binance.fapiPrivate_post_leverage({
    'symbol' : market['id'],
    'leverage' : leverage
})

btc_ohlcv = binance.fetch_ohlcv("BTC/USDT") # 1분봉 조회
balance = binance.fetch_balance() #잔고 조회params={'type': 'future'}
# positions = balance['info']['positions'] #포지션 얻기
# for position in positions:
#     if position["symbol"] == "BTCUSDT":
#         pprint.pprint(position)


# pprint.pprint(binance.fetch_ticker("BTC/USDT")) # 현재 진행되고있는 봉에 대해 알수있음
# btc_ohlcv = binance.fetch_ohlcv("BTC/USDT", '1d') # 일봉 조회
# pprint.pprint(binance.fetch_ticker("BTC/USDT")['last']) 실시간 현재가


#과거 데이터 조회
df = pd.DataFrame(btc_ohlcv, columns = ['datetime', 'open', 'high', 'low', 'close', 'volume'])
df['datetime'] = pd.to_datetime(df['datetime'], unit = 'ms')
df.set_index('datetime', inplace = True)

print(df)
#선물 Orderbook
# orderbook = binance.fetch_order_book("BTC/USDT")
# asks = orderbook['asks']
# bids = orderbook['bids']

#주문(시장가)
# order_long = binance.create_market_buy_order(
#     symbol = "BTC/USDT",
#     amount = 0.001
# )

# order_short = binance.create_market_sell_order(
#     symbol = "BTC/USDT",
#     amount = 0.001
# )

#주문(지정가)
# limit_long = binance.create_limit_buy_order(
#     symbol = "BTC/USDT",
#     amount = 0.001,
#     price = 16000
# )

# limit_short = binance.create_limit_sell_order(
#     symbol = "BTC/USDT",
#     amount = 0.001,
#     price = 16000
# )
#대기 주문 조회
# open_orders = binance.fetch_open_orders(
#     symbol = "BTC/USDT"
# )

