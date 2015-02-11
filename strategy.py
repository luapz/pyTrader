# -*- coding: utf-8 -*-
import random
from event import OrderEvent


class TestRandomStrategy(object):
    def __init__(self, symbol, units, events):
        self.symbol = symbol
        self.units = units
        self.events = events
        self.ticks = 0

    def calculate_signals(self, event):
        if event.type == 'TICK':
            self.ticks += 1
            if self.ticks % 5 == 0:
                side = random.choice(["buy", "sell"])
                order = OrderEvent( self.symbol, self.units, "market", side )
                self.events.put(order)