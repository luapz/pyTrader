# -*- coding: utf-8 -*-
from settings import server, port, servertype, showcerterror, user, password, certpw, account_number, account_pw
from streaming import StreamingXing
from strategy import TestRandomStrategy
from execution import Execution
from xaevents import XASession, XARealEvents, XAReal
from queue import Queue
from threading import Thread
import pythoncom
import time


class trade(Thread):
    def __init__(self, heartbeat, que, strategy, execution):
        Thread.__init__(self)
        self.que = que
        self.heartbeat = heartbeat
        self.strategy = strategy
        self.execution = execution

    def run(self):

        while True:
            if self.que.empty():
                pass
            else:
                event = self.que.get()
                if event.type == 'TICK':
                        print (event.symbol, event.time, event.bid, event.ask, event.price)
                        self.strategy.calculate_signals(event)
                elif event.type == 'ORDER':
                        print ("Executing order!")
                        self.execution.execute_order(event)

            time.sleep(heartbeat)


if __name__ == '__main__':

    XASession.connectXing(server, port, user, password, certpw, servertype, showcerterror)

    units = 1
    heartbeat = 0.01
    #symbols = ['005930', '005380', '066570', '035720', '000660']
    symbols = ['005930', '005380']
    priceq = {}; roopq ={}; price = {}; roop = {}; strategy = {}

    for i in range(1, len(symbols)+1 ):    #  멀티플 큐 생성
        priceq["priceq{0}".format(i)] = Queue(1000)
        strategy["strategy{0}".format(i)] = TestRandomStrategy(symbols[i-1], units, priceq["priceq{0}".format(i)])

    execution = Execution(account_number, account_pw, XASession)

    for i in range(1,len(symbols)+1):   # 멀티플 데이터 스트림 스래드 생성
        price["price{0}".format(i)] = StreamingXing(XAReal, XARealEvents, symbols[i-1], 'shcode', 'S3_', priceq["priceq{0}".format(i)])
        roop["roop{0}".format(i)] = trade(heartbeat, priceq["priceq{0}".format(i)], strategy["strategy{0}".format(i)], execution)

    for i in range(1,len(symbols)+1):   #셋 데몬 & 런
        price["price{0}".format(i)].setDaemon(True)
        roop["roop{0}".format(i)].setDaemon(True)
        price["price{0}".format(i)].start()
        roop["roop{0}".format(i)].start()


    while True:
        pythoncom.PumpWaitingMessages()


