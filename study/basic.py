# 주석
'''
한줄 주석 : #
여러줄 주석 : [작은따음표or큰따음표]x3 내용 [작은따음표or큰따음표]x3
파이썬에선 주석도 들여쓰기를 맞춰서 해줘야한다 어떤 함수의 주석인지 확인하기 위해
'''

# range(연속된 숫자 생성)
'''
a = list[range(10)] : 0부터 인자값-1 만큼의 연속된 숫자 생성
    0 ~ 9
b = list(range(3, 7)) : 첫번째 인자값부터 마지막 인자값-1 만큼의 숫자 생성
    3 ~ 6
'''

# dataType(자료형)
'''
정수 : int
실수 : float
문자열 : str
true, false : bool

list() : 리스트
    리스트명 = [요소1, 요소2, 요소3, ...]
    a = list()
    리스트안에 어떠한 자료형이든 포함가능
    a[-1] 이렇게 하면 마지막 요소 호출 
    [-2], [-3], ... 이렇게하면 뒤에서부터 호출하는듯
    len(a) 길이 구하기
    데이터 추가 : b = []
        b.append('데이터')
    정렬 : sorted(a) = 오름차순으로 정렬

tuple() : 튜플
    리스트와 비슷하지만 ()로 생성
    t = (1, 2, 3, 4)
    t = (1, ) 1개 요소사용시 콤마가 꼭 필요
    튜플은 값이 변하지않는 고정된값을 사용할때 이용 

dict() : 딕셔너리
    Java HashMap처럼 Key : Value로 이루어짐
    d = {Key1 : Value1, Key2 : Value2, ...}
    데이터 추가 : d['name'] = 'Hyoboy'
    데이터 삭제 : del d['name']

슬라이싱 :
    a[0:4], a[:4] = 1번째 인덱스부터 출력할수있음
    a[3:], a[3:6] = 3번째 인덱스부터 호출도 가능
'''

# 반복문
'''
for 변수 in Sequence(str, list, tuple, range, ...) : 

Sequence는 반복 가능한 형태 문자열도 가능함
'''

# self, id()
'''
클래스 혹은 메서드의 첫번째 변수로 self 사용
객체 자신을 나타낸다. Java this처럼 이용

id()는 객체의 고유값을 호출해주는 내장함수
print(f"val :: {id(self)}") 처럼 사용
'''

# import, from
'''
math 모듈을 사용하고싶을때
import math
math.max(1, 2, 3)

math 모듈안의 함수 하나만 선언할때
from math import math
max(1, 2, 3) 바로사용 가능

혹은 
from math import *
이렇게 선언하면 함수만가지고 바로 사용가능
max(1, 2, 3) 
'''

# 패키지 다운로드, 업그레이드 등
'''
다운로드
pip install '패키지 이름'

업그레이드
pip install --upgrade '패키지 이름'

삭제
pip uninstall '패키지 이름'

설치된 패키지 리스트
pip list
'''