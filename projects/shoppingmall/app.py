from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

#import requests
#from bs4 import BeautifulSoup

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('index.html')

@app.route('/orders', methods=['GET'])
def listing():
    result = list(db.orders.find({},{'_id':False}))# 1. 모든 document 찾기 & _id 값은 출력에서 제외하기
    return jsonify({'result':'success','orders':result, 'msg':'출력하기 위해 db로부터 데이터 전송 완료받았습니다'})
    # 2. orders라는 키 값으로 주문입력정보 내려주기
    

@app.route('/orders', methods=['POST'])
def saving():
    # 1. 클라이언트로부터 데이터를 받기
    name_receive = request.form['name_give'] #여기에 html에 정의한 url값이 받아지는거야, 그걸 찾아내는 키값이 url_give인거고
    amount_receive = request.form['amount_give']
    address_receive = request.form['address_give']
    phone_receive = request.form['phone_give']


    # 2. orders라는 컬렉션에 데이터 넣기
    order={'name':name_receive , 'amount':amount_receive , 'address':address_receive, 'phone':phone_receive}
    db.orders.insert_one(order)

    return jsonify({'result':'success', 'msg':'저장되었습니다!'})


if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)