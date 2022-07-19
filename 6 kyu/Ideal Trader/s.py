610ab162bd1be70025d72261


def ideal_trader(prices):
    res = 1
    for i in range(1, len(prices)):
        if prices[i] > prices[i-1]:
            res *= prices[i]/prices[i-1]
    return res
__________________________________
from numpy import*;ideal_trader=lambda p:exp(sum(maximum(diff(log(p)),0)))
__________________________________
import math
def ideal_trader(prices):
    roi = 1

    # Either we look to buy at next local minimum
    # or looking to sell at the next local maximum.
    looking_to_buy = True

    # Adding a -1 price point at the end to ensure we sell at the end.
    for curr, future in zip(prices, prices[1:] + [-1]):
        if looking_to_buy and future > curr:
            # Lets buy before price goes up!
            start_price = curr
            looking_to_buy = False
        elif not looking_to_buy and curr > future:
            # Lets sell before the price goes down!
            roi *= (curr/start_price)
            looking_to_buy = True
    return roi
__________________________________
from itertools import pairwise
from math import prod

def ideal_trader(prices):
    return prod(max(q / p, 1) for p, q in pairwise(prices))
__________________________________
def ideal_trader(prices):
    fiat=1
    stonks=0    
    for i in range(1,len(prices)):
        if fiat>0 and prices[i]>prices[i-1]:
            stonks=(fiat/prices[i-1])
            fiat=0
        if stonks>0 and prices[i]<prices[i-1]:
            fiat=stonks*prices[i-1]
            stonks=0    
    return max([stonks*prices[-1], fiat])
__________________________________
def f_buy(arr):
    candidat = arr[0]
    for num, i in enumerate(arr[1:], 1):
        if candidat >= i:
            candidat = i
        else:
            return candidat, arr[num:]
    return None, []
        
        
def f_sell(arr):
    candidat = arr[0]
    for num, i in enumerate(arr[1:], 1):
        if candidat <= i:
            candidat = i
        else:
            return candidat, arr[num:]
    return candidat, []
                                 

def ideal_trader(prices):
    if len(set(prices)) == 1:
        return 1
    l = []
    while prices:
        tmp = []
        buy, prices = f_buy(prices)
        tmp.append(buy)
        if prices:
            sell, prices = f_sell(prices)
            tmp.append(sell)
        if tmp != [None]:
            l.append(tmp)
    res = 1
    for a, b in l:
        res = (b * res) / a
    return res
__________________________________
from operator import mul
from functools import reduce

def ideal_trader(prices):
    return reduce(mul, [b/a for a, b in zip(prices, prices[1:]) if a < b], 1)
__________________________________
def ideal_trader(prices):
    money = 1
    for i in range(1, len(prices)):
        if prices[i] > prices[i - 1]:
            money *= prices[i] / prices[i - 1]
    return money
__________________________________
def ideal_trader(prices):
    money = 1
    for i in range(1, len(prices)):
        if prices[i] > prices[i - 1]:
            money *= prices[i] / prices[i - 1]
    return money
__________________________________
def ideal_trader(prices):
    deposit = 1
    buy_in = prices[0]
    max_current_price = prices[0]
    profit = 0
    for current_price in prices:
        if current_price > max_current_price :
            max_current_price = current_price
        if current_price < max_current_price or current_price == prices[len(prices ) - 1]:
            profit = max_current_price / buy_in
            buy_in = max_current_price = current_price
            deposit *= profit
    return deposit
__________________________________
import math

def ideal_trader(prices):
    i = 0 
    min = 0 
    max = 0 
    result = []
    while i < (len(prices) - 1):
        if prices[i] <= prices [i+1]:
            if min == 0 :
                min = prices[i]
            if max < prices[i+1]:
                max = prices[i+1]

        elif prices[i] > prices [i+1]:
            if max > 0 or min > 0:
                result.append(max/min)
            min = 0
            max = 0

        i += 1
    if max > 0 or min > 0:
        result.append(max/min)

    profit = math.prod(result)
    
    return profit
__________________________________
def ideal_trader(prices):
    fiat=1
    stonks=0    
    for i in range(1,len(prices)):
        if fiat>0 and prices[i]>prices[i-1]:
            stonks=(fiat/prices[i-1])
            fiat=0
        if stonks>0 and prices[i]<prices[i-1]:
            fiat=stonks*prices[i-1]
            stonks=0    
    return max([stonks*prices[-1], fiat])
