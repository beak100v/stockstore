import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.stocksstore02


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

db.stocks.delete_many({})

for num in range(1, 2):
    url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0&page=" + str(num)
    data = requests.get(url,headers=headers)
# data = requests.get('https://finance.naver.com/sise/sise_market_sum.nhn', headers=headers)
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
#
# for num in range(1, 33):
#     url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=1&page=" + str(num)
#     data = requests.get(url,headers=headers)
# # data = requests.get('https://finance.naver.com/sise/sise_market_sum.nhn', headers=headers)
#     soup = BeautifulSoup(data.text, 'html.parser')
#     stocks = soup.select('#contentarea > div.box_type_l > table.type_2 > tbody > tr')
#     for stock in stocks:
#         name = stock.select_one('td:nth-child(2) > a')
#         if name is not None:
#             price = stock.select_one('td:nth-child(3)').text
#             total = stock.select_one('td:nth-child(7)').text
#             doc = {
#                 'name': name.text,
#                 'price': price,
#                 'total': total
#             }
#             db.stocks.insert_one(doc)

@app.route('/')
def stocks_store():
    return render_template('page_one.html')

@app.route('/page_two')
def stocks_store_page_2():
    return render_template('page_two.html')


@app.route('/api/list', methods=['GET'])
def show_stocks():
    stock_rank = list(db.stocks.find({}, {'_id': 0}))
    return jsonify({'result': 'success','stocks_list':stock_rank})


if __name__ == '__main__':
    app.run('0.0.0.0', port=12345, debug=True)

