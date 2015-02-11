# -*- coding: utf-8 -*-

class Event(object):
    pass

class TickEvent(Event):
    def __init__(self, symbol, time, bid, ask, price):
        self.type = 'TICK'
        self.symbol = symbol
        self.time = time
        self.bid = bid
        self.ask = ask
        self.price = price

class OrderEvent(Event):
    def __init__(self, symbol, units, order_type, side):
        self.type = 'ORDER'
        self.symbol = symbol
        self.units = units
        self.order_type = order_type
        self.side = side
