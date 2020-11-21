from bs4 import BeautifulSoup
from pprint import pprint
import requests

#웹 페이지를 열고 소스코드를 읽어오는 작업
html = requests.get("http://comic.naver.com/webtoon/weekday.nhn")
soup = BeautifulSoup(html.text, 'html.parser')
html.close()

#월요웹툰영역 추출하기
data1=soup.find('div',{'class':'col_inner'})
#pprint(data1)
data1_list=soup.findAll('div',{'class':'col_inner'})
#제목 포함영역 추출하기
data2=data1.findAll('a',{'class':'title'})
pprint(data2)
print(data1)
#이번에는 어떤 수정을 해 볼까나 재미있네
