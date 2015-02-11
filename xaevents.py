
import win32com.client
import pythoncom
from event import *


class XAEvent(object):
    pass

class XASession(object):

    def connectXing(server, port, user, password, certpw, servertype, showcerterror):

        XASession = win32com.client.DispatchWithEvents("XA_Session.XASession",XASessionEvents)
        XASession.ConnectServer(server, port)
        XASession.Login(user, password, certpw, servertype, showcerterror)

        while XASessionEvents.logInState == 0:
            pythoncom.PumpWaitingMessages()

class XASessionEvents(XAEvent):
    logInState = 0
    def OnLogin(self, code, msg):
        print("OnLogin method is called")
        print(str(code))
        print(str(msg))
        if str(code) == '0000':
            XASessionEvents.logInState = 1
    def OnLogout(self, *args):
        print ("OnLogout", args)
    def OnDisconnect(self, *args):
        print ("OnDisconnect", args)

class XARealEvents(XAEvent):    #스레딩생성용
    def OnReceiveRealData(self, *args):
        symbol = self.GetFieldData( 'OutBlock', 'shcode' )
        time = self.GetFieldData( 'OutBlock', 'chetime' )
        bid =  self.GetFieldData( 'OutBlock', 'bidho' )
        ask =  self.GetFieldData( 'OutBlock', 'offerho' )
        price = self.GetFieldData( 'OutBlock', 'price' )
        #localtime = str(datetime.datetime.now().time())
        tev = TickEvent(symbol, time, bid, ask, price)
        self.que.put(tev)

class XAReal(XAEvent):
    def __init__(self, que):
        self.que = que


class XAQueryEvents(XAEvent):
    queryState = 0
    def OnReceiveData(self, szTrCode):
        print("ReceiveData")
        XAQueryEvents.queryState = 1
    def OnReceiveMessage(self, systemError, mesageCode, message):
        print("ReceiveMessage")
        print(message)



