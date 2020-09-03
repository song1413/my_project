from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request
from datetime import datetime
import schedule
import time

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta


# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('cover.html')


@app.route('/main')
def main():
    return render_template('main.html')


@app.route('/bookadd1')
def bookAdd1():
    return render_template('bookAdd1.html')


@app.route('/bookadd2')
def bookAdd2():
    temp = request.args.get('isbn')
    return render_template(
        'bookAdd2.html', isbn=temp)


@app.route('/library', methods=['GET'])
def library():
    return render_template('library.html')




## API 역할을 하는 부분
@app.route('/booksave', methods=['POST'])
def addBook():
    # 1. 클라이언트가 준 title, author, review 가져오기.
    thumbnail_receive = request.form['thumbnail_give']
    title_receive = request.form['title_give']
    authors_receive = request.form['authors_give[]']
    publisher_receive = request.form['publisher_give']
    datetime_receive = request.form['datetime_give']
    isbn_receive = request.form['isbn_give']
    page_receive = request.form['page_give']
    contents_receive = request.form['contents_give']
    key_receive = datetime.today().strftime("%Y%m%d%H%M%S")


    # 2. DB에 정보 삽입하기
    book = {
        'thumbnail': thumbnail_receive,
        'title': title_receive,
        'authors': authors_receive,
        'publisher': publisher_receive,
        'datetime': datetime_receive,
        'isbn': isbn_receive,
        'page': page_receive,
        'contents': contents_receive,
        'key': key_receive,
    }

    # 3. books에 book 저장하기
    db.books.insert_one(book)


    # 4. 성공 여부 & 성공 메시지 반환하기
    return jsonify({'result': 'success'})



@app.route('/booksave/edit', methods=["POST"])
def edit_booksave():
    key_receive = request.form['key_give']
    page_receive = request.form['page_give']
    contents_receive = request.form['contents_give']

	# key 기준으로 메시지를 찾아 내용과 생성 시각을 업데이트합니다.
    db.books.update_one({'key': key_receive}, {'$set': {'page': page_receive, 'contents': contents_receive}})

    return jsonify({'result': 'success', 'msg': '메시지 변경에 성공하였습니다!'})



@app.route('/booksave', methods=['GET'])
def read_books():
    # 1. mongodb에서 모든 데이터 조회해오기 (read)
    result = list(db.books.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'books':result})



@app.route('/bookadd4')
def bookAdd4():
    return render_template('bookAdd4.html')


# def job():
#     result = list(db.books.find({}, {'_id': 0}))
#
# schedule.every().day.at("00:00").do(job)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
