total_balance = 5000
user_price = 10000
count=1
price=5000
betSize_per = total_balance/5
betSize = betSize_per/price
pre_betSize = betSize_per/user_price

user_price = (user_price*pre_betSize + price*betSize)/(pre_betSize+betSize)
#                                                       다음 런에서 분모가 pre_betSize가 됨
print(user_price)