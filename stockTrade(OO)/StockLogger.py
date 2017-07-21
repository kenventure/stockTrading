
from Logger import Logger

class StockEntry:
    def __init__(self):
        None
    name=""
    long=False
    buy=False
    price=0
    
class StockLogger(Logger):
    def __init__(self, filename):
        Logger.__init__(self, filename)
        self.file.write("Name,Buy,Long,Price\n")
    def log(self, stockEntry):
        self.file.write(stockEntry.name+","+str(stockEntry.buy)+","+"-"+","+str(stockEntry.price)+"\n")