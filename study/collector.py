# DB 커넥션 테스트
# MySQL 사용

from sqlalchemy import create_engine
import pymysql
# MySQLdb 모듈이 없다고 나올경우 아래있는 코드 이용
pymysql.install_as_MySQLdb()

class Collector :
    def __init__(self) :
        self.engine_bot = None

    def setting(self, db_name, db_id, db_passwd, db_ip, db_port) :
        # MySQL 연동
        self.engine_bot = create_engine('mysql+mysqldb://' + db_id + ':' + db_passwd + '@' + db_ip + ':' + db_port + '/' + db_name, encoding='utf-8')

if __name__ == '__main__' :
    # 메인으로 실행될경우
    col = Collector()
    
    # 생성한 DB이름
    db_name = '생성한 DB이름'
    # 로그인 계정
    db_id = '로그인 계정'
    # DB IP
    db_ip = '127.0.0.1'
    # 패스워드
    db_passwd = '패스워드'
    # 설정한 포트
    db_port = '3306'

    # 세팅 호출
    col.setting(db_name, db_id, db_passwd, db_ip, db_port)

    # 쿼리
    sql = "select * from bot_test.class1;"

    # 실행한 결과
    rows = col.engine_bot.execute(sql).fetchall()
    print(rows)