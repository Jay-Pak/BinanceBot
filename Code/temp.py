user_price = 10000
pre_betSize = 2000

current_price = 20000
betSize = 1000



user_price = ((user_price * pre_betSize) + (current_price * betSize)) / (pre_betSize + betSize)

pre_betSize += betSize

print(user_price, pre_betSize)