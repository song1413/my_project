from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request

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
        'bookAdd2.html',isbn=temp)

## API 역할을 하는 부분
@app.route('/booksave', methods=['POST'])
def addBook():
	# 1. 클라이언트가 준 title, author, review 가져오기.
    thumbnail_receive = request.form['thumbnail_give']
    title_receive = request.form['title_give']
    authors_receive = request.form['authors_give']
    publisher_receive = request.form['publisher_give']
    datetime_receive = request.form['datetime_give']
    isbn_receive = request.form['isbn_give']

	# 2. DB에 정보 삽입하기
    book = {
        'thumbnail': thumbnail_receive,
        'title': title_receive,
        'authors': authors_receive,
        'publisher': publisher_receive,
        'datetime': datetime_receive,
        'isbn': isbn_receive
    }

    # 3. books에 book 저장하기
    db.books.insert_one(book)

	# 4. 성공 여부 & 성공 메시지 반환하기
    return jsonify({'result': 'success', 'msg': '책장에 등록되었습니다'})

@app.route('/booksave', methods=['GET'])
def read_books():
    return jsonify({'result': 'success', 'msg': '이 요청은 GET!'})


@app.route('/bookadd4')
def bookAdd4():
    return render_template('bookAdd4.html', )



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)