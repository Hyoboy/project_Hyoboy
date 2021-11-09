import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from pandas import DataFrame
import time

class OpenApi(QAxWidget) :
    def __init__(self) :
        super().__init__()
        # 환경체크
        self.checkEnv()
        # 키움증권 인스턴스
        self.createKiwoomInstance()
        # 키움증권 이벤트처리
        self.set_signal_slots()
        # 키움증권 로그인
        self.CommConnect()
        # 키움증권 계좌정보
        self.accountInfo()
        # 테스트용 삼성전자 주가정보 호출
        self.getDailyData()


    # 데이터 세팅
    def setData(self, id, val) :
        self.dynamicCall("SetInputValue(QString, QString)", id, val)

    # 종목코드 데이터 호출
    def getTotalData(self, code, endDt) :
        # 초기화
        self.ohlcv = {'date' : [], 'open' : [], 'high' : [], 'low' : [], 'close' : [], 'volume' : []}
        # 호출할 데이터 세팅
        self.setData("종목코드", code)
        self.setData("기준일자", endDt)
        self.setData("수정주가구분", 1)
        self.commReqData("opt10081_req", "opt10081", 0, "0101")

        # 왜 전체 데이터 호출이 안됨??
        while self.remained_data == True :
            self.setData("종목코드", code)
            self.setData("기준일자", endDt)
            self.setData("수정주가구분", 1)
            self.commReqData("opt10081_req", "opt10081", 2, "0101")

        time.sleep(0.5)
        # data 비어있는 경우
        if len(self.ohlcv) == 0 :
            return []

        if self.ohlcv['date'] == '' :
            return []

        df = DataFrame(self.ohlcv, columns=['open', 'high', 'low', 'close', 'volume'], index=self.ohlcv['date'])

        return df

    def commReqData(self, rqname, trcode, next, screen_no) :
        self.dynamicCall("CommRqData(QString, QString, int, QString)", rqname, trcode, next, screen_no)
        # 딜레이 꼭 필요 없으면 데이터호출이 안되는 현상 (나중에 다시 공부)
        time.sleep(0.5)
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()

    # 데이터 호출
    def getDailyData(self) :
        # 종목코드, 데이터 가져올 마지막 날짜
        print('데이터 호출중입니다...')
        data = self.getTotalData('005930', '20211107')
        print(data)

    def getLoginInfo(self, tag) :
        try :
            rtn = self.dynamicCall("GetLoginInfo(QString)", tag)
            return rtn
        except Exception as e :
            print(e)

    def accountInfo(self) :
        account_number = self.getLoginInfo('ACCNO')
        self.account_number = account_number.split(';')[0]
        print('계좌번호 : ' + self.account_number)

    def createKiwoomInstance(self) :
        # 키움증권 인스턴스 생성
        self.setControl('KHOPENAPI.KHOpenAPICtrl.1')

    def set_signal_slots(self) :
        try :
            self.OnEventConnect.connect(self.eventConnect)
            self.OnReceiveTrData.connect(self.receiveTrData)
        except Exception as e :
            print(e)
        
    def getCommData(self, code, field_name, index, item_name):
        ret = self.dynamicCall("GetCommData(QString, QString, int, QString)", code, field_name, index, item_name)
        return ret.strip()

    def getRepeatCnt(self, trcode, rqname):
        ret = self.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
        return ret

    def opt10081(self, rqname, trcode) :
        # 반복횟수 설정
        ohlcvCnt = self.getRepeatCnt(trcode, rqname)
        
        # 데이터 추가
        for i in range(ohlcvCnt) :
            date = self.getCommData(trcode, rqname, i, "일자")
            open = self.getCommData(trcode, rqname, i, "시가")
            high = self.getCommData(trcode, rqname, i, "고가")
            low = self.getCommData(trcode, rqname, i, "저가")
            close = self.getCommData(trcode, rqname, i, "현재가")
            volume = self.getCommData(trcode, rqname, i, "거래량")

            self.ohlcv['date'].append(date)
            self.ohlcv['open'].append(int(open))
            self.ohlcv['high'].append(int(high))
            self.ohlcv['low'].append(int(low))

            self.ohlcv['close'].append(int(close))
            self.ohlcv['volume'].append(int(volume))

    # 데이터 호출 이벤트처리
    def receiveTrData(self, screen_no, rqname, trcode, record_name, next, etc1, etc2, etc3, etc4) :
        #print(screen_no, rqname, trcode, record_name, next)

        if next == '2' :
            self.remained_data = True
        else:
            self.remained_data = False

        # 이벤트 정리
        #print('rqname : ' + rqname)
        if rqname == "opt10081_req" :
            self.opt10081(rqname, trcode)

        # 이벤트 종료
        self.tr_event_loop.exit()


    # 로그인 이벤트처리
    def eventConnect(self, errCode) :
        if errCode == 0 :
            print('로그인 성공')
        elif errCode == -100 :
            # 사용자 처리 실패
            print('실패')
        elif errCode == -101 :
            # 서버 연결 실패
            print('실패')
        # 이벤트루프 종료
        self.login_event_loop.exit()

    def CommConnect(self) :
        try :
            # 로그인
            self.dynamicCall('CommConnect()')
            # 로그인 후 데이터처리 대기코드 (아래코드없이 실행하면 로그인처리 후 바로 코드가 실행되어 서비스 종료됨)
            self.login_event_loop = QEventLoop()
            # event loop 전처리
            # 여기 지우고 사용
            #
            self.login_event_loop.exec_()
            # event loop 후처리
            # 여기 지우고 사용
            #
        except Exception as e :
            print(e)

    def checkEnv(self) :
        is_64bit = sys.maxsize > 2 ** 32
        if is_64bit :
            print('HTS는 32Bit 환경만 지원하고있습니다.\n32Bit 환경에서 실행해주세요.')

if __name__ == "__main__" :
    # QApplication Class 인스턴스 생성 (sys.argv : 파일의 절대경로)
    app = QApplication(sys.argv)
    # event loop
    OpenApi()