import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.stocksstore

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://finance.naver.com/sise/sise_market_sum.nhn?sosok=1', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

stocks = soup.select('#contentarea > div.box_type_l > table.type_2 > tbody > tr')

for stock in stocks:
    name = stock.select_one('td:nth-child(2) > a')
    if name is not None:
        price = stock.select_one('td:nth-child(3)').text
        total = stock.select_one('td:nth-child(7)').text
        doc = {
            'name': name.text,
            'price': price,
            'total': total
        }
        db.stocks.insert_one(doc)
#이건 이제 필요 없는 파일인가

#23dlf 두번째 테스느
