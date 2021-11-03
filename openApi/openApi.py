import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *

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
        self.account_info()

    def getLoginInfo(self, tag):
        try:
            rtn = self.dynamicCall("GetLoginInfo(QString)", tag)
            return rtn
        except Exception as e:
            print(e)

    def account_info(self):
        account_number = self.getLoginInfo('ACCNO')
        print(account_number)
        self.account_number = account_number.split(';')[0]
        print('계좌번호 : ' + self.account_number)

    def createKiwoomInstance(self) :
        # 키움증권 인스턴스 생성
        self.setControl('KHOPENAPI.KHOpenAPICtrl.1')

    def set_signal_slots(self) :
        try :
            self.OnEventConnect.connect(self.eventConnect)
        except Exception as e :
            print(e)
        
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