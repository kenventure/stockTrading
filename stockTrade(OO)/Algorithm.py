

class Algorithm (object):
    def __init__(self, intervalMin):
        raise NotImplementedError("Subclass must implement abstract method")	
    def trade(self, time, price):
        raise NotImplementedError("Subclass must implement abstract method")

    def isBuy():
        raise NotImplementedError("Subclass must implement abstract method")

    def isSell():
        raise NotImplementedError("Subclass must implement abstract method")

