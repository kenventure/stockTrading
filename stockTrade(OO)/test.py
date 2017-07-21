

from StockLogger import StockLogger
from StockLogger import StockEntry

logger = StockLogger('test.txt')

entry = StockEntry()

entry.name="HandSeng"
entry.long=True

entry.buy = True
entry.price = 1.38

logger.log(entry)

entry.price=1.8

entry.buy=False

logger.log(entry)