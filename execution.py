import win32com.client
from xaevents import XAQueryEvents

class Execution:

    def __init__(self, account_number, account_pw, XASession):
        self.account_number = account_number
        self.account_pw = account_pw
        self.XAQuery_order = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
        self.XAQuery_order.LoadFromResFile("C:\\ETRADE\\xingAPI\\Res\\CSPAT00600.res")
        self.XASession = XASession

    def execute_order(self, event):
        self.XAQuery_order.SetFieldData("CSPAT00600InBlock1", 'AcntNo', 0, self.account_number)
        self.XAQuery_order.SetFieldData("CSPAT00600InBlock1", 'InptPwd', 0, self.account_pw)
        self.XAQuery_order.SetFieldData("CSPAT00600InBlock1", 'IsuNo', 0, 'A'+ event.symbol)
        self.XAQuery_order.SetFieldData("CSPAT00600InBlock1", 'OrdQty', 0, event.units) #수량

        if event.order_type == 'market':    #지정가일 경우 가격을, 시장가일 경우 0 을 입력
            OrdPrc = 0
            OrdprcPtnCode = '03'
        elif event.order_type == 'stop':
            OrdPrc = event.orderprice
            OrdprcPtnCode = '00'
        self.XAQuery_order.SetFieldData("CSPAT00600InBlock1", 'OrdPrc', 0, OrdPrc)

        if event.side == 'buy':     #매도 1 매수 2
            BnsTpCode = 2
        elif event.side == 'sell':
            BnsTpCode = 1
        self.XAQuery_order.SetFieldData("CSPAT00600InBlock1", 'BnsTpCode', 0, BnsTpCode)

        #지정가 00, 시장가 03, 조건부지정가 05, 최유리지정가 06, 최우선지정가 07, 장개시전시간외 61, 시간외종가 81, 시간외단일가 82
        self.XAQuery_order.SetFieldData("CSPAT00600InBlock1", 'OrdprcPtnCode', 0, OrdprcPtnCode)
        self.XAQuery_order.SetFieldData("CSPAT00600InBlock1", 'MgntrnCode', 0, '000')
        self.XAQuery_order.SetFieldData("CSPAT00600InBlock1", 'LoanDt', 0, '0')
        self.XAQuery_order.SetFieldData("CSPAT00600InBlock1", 'OrdCndiTpCode', 0, '0')

        XAQueryEvents.session =  self.XASession

        ret = self.XAQuery_order.Request(False) ## XING API 에러처리

        if ret < 0 :
            print(self.XASession.GetErrorMessage(self.XASession.GetLastError()))