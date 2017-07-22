
from Logger import Logger
import datetime

class StockEntry:
    def __init__(self):
        None
    name=""
    long=False
    buy=False
    price=0
    RSI=0
    
class StockLogger(Logger):
    def __init__(self, filename):
        Logger.__init__(self, filename)
        self.file.write("Time,Name,Buy,Long,Price,RSI\n")
    def log(self, stockEntry):
        if stockEntry.buy is True:
            b = 'Buy'
        else:
            b = 'Sell'
        self.file.write(str(datetime.datetime.now())+","+stockEntry.name+","+b+","+"-"+","+str(stockEntry.price)+","+str(stockEntry.RSI)+"\n")