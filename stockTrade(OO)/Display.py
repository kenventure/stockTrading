class Display (object):
    def __init__(self):
        raise NotImplementedError("Subclass must implement abstract method")	
    def display(self, arr, anno, price, rsi):
        raise NotImplementedError("Subclass must implement abstract method")
    def log(self, arr, anno, price):
        raise NotImplementedError("Subclass must implement abstract method")
    