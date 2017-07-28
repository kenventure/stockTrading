

from StockLogger import StockLogger
from StockLogger import StockEntry
from OpenCloseCheck import OpenCloseCheck
import datetime

logger = StockLogger('test.txt')

entry = StockEntry()

entry.name="HandSeng"
entry.long=True

entry.buy = True
entry.price = 1.38
entry.RSI=10

logger.log(entry)
entry.RSI=65
entry.price=1.8

entry.buy=False

logger.log(entry)


openTime=datetime.time(14,0,0,0)
closeTime=datetime.time(15,0,0,0)
clearTime=datetime.time(15,4,0,0)

openCheck = OpenCloseCheck(openTime, closeTime, clearTime)

print(openCheck.isOpen())

print(openCheck.isClear())