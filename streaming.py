# -*- coding: utf-8 -*-

import win32com.client
from threading import Thread

class StreamingXing(Thread):    # 스레딩생성용
    def __init__(self, XAReal, XARealEvents, instrument, inblock, Res, que):
        Thread.__init__(self)
        self.XAReal = XAReal
        self.XARealEvents = XARealEvents
        self.instrument = instrument
        self.inblock = inblock
        self.Res = Res
        self.que = que
        self.XAReal = win32com.client.DispatchWithEvents("XA_DataSet.XAReal", XARealEvents)
        self.XAReal.LoadFromResFile("C:\\ETRADE\\xingAPI\\Res\\%s.res" % self.Res)
        self.XAReal.SetFieldData('InBlock', self.inblock, self.instrument)
        self.XAReal.que = self.que
        self.XAReal.AdviseRealData()