from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request
from datetime import datetime
import schedule
import time
import random

app = Flask(__name__)

client = MongoClient('mongodb://todaysbook:todaysbook@localhost', 27017)
db = client.dbsparta


# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('cover.html')


@app.route('/main')
def main():
    if db.books.count_documents({}) == 0:
        random_sentence = {'title': '책 제목', 'page': '책 페이지',
                           'content': '여기에 내용이 표시됩니다 :)'}
        return render_template('main.html', sentence=random_sentence)
    else:
        choice_book = random.choice(list(db.books.find({'sentences': {'$not': {'$size': 0}}})))  # sentences가 없는 경우는 제외
        choice_sentence = random.choice(list(choice_book['sentences']))
        random_sentence = {'title': choice_book['title'], 'page': choice_sentence['page'],
                           'content': choice_sentence['content']}
        return render_template('main.html', sentence=random_sentence)



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

    sentence = {'page': page_receive, 'content': contents_receive, 'key': key_receive, 'created_at': datetime.now()}

    # 2. DB에 정보 삽입하기
    insert_book = {
        'thumbnail': thumbnail_receive,
        'title': title_receive,
        'authors': authors_receive,
        'publisher': publisher_receive,
        'datetime': datetime_receive,
        'isbn': isbn_receive,
        'sentences': [sentence],
        'created_at': datetime.now()
    }
    # 3. books에 select_book 저장하기
    select_book = db.books.find_one({'isbn': isbn_receive}, {'_id': 0})

    if select_book is None:
        db.books.insert_one(insert_book)
    else:
        update_sentences = list(select_book['sentences'])
        update_sentences.append(sentence)
        db.books.update_one({'isbn': isbn_receive}, {'$set': {'sentences': update_sentences}})
    # 4. 성공 여부 & 성공 메시지 반환하기
    return jsonify({'result': 'success'})




@app.route('/sentences', methods=['GET'])
def getSentences():
    isbn_receive = request.args.get('isbn_give')
    book = db.books.find_one({'isbn':isbn_receive},{'_id':0})
    if book is not None:
        return jsonify({'result': 'success', 'sentences': book['sentences']})
    else:
        return jsonify({'result': 'success', 'sentences': []})

@app.route('/booksave/edit', methods=["POST"])
def edit_booksave():
    key_receive = request.form['key_give']
    page_receive = request.form['page_give']
    contents_receive = request.form['content_give']
    isbn_receive = request.form['isbn_give']

    select_book = db.books.find_one({'isbn': isbn_receive}, {'_id': 0})
    update_sentences = list(select_book['sentences'])
    for sentence in update_sentences:
        if sentence['key'] == key_receive:
            sentence['page'] = page_receive
            sentence['content'] = contents_receive

    db.books.update_one({'isbn': isbn_receive}, {'$set': {'sentences': update_sentences}})

    return jsonify({'result': 'success', 'msg': '메시지 변경에 성공하였습니다!'})


@app.route('/booksave/delete', methods=["POST"])
def delete_booksave():
    key_receive = request.form['key_give']
    isbn_receive = request.form['isbn_give']
    select_book = db.books.find_one({'isbn': isbn_receive}, {'_id': 0})
    delete_sentences = list(select_book['sentences'])
    for idx, sentence in enumerate(delete_sentences):
        if sentence['key'] == key_receive:
            delete_sentences.pop(idx)  #key값을 가진 sentences를 삭제해라
    db.books.update_one({'isbn': isbn_receive}, {'$set': {'sentences': delete_sentences}})  #sentences가 업데이트 된 book을 업데이트 해라
    return jsonify({'result': 'success'})


@app.route('/book/delete', methods=["POST"])
def delete_book():
    isbn_receive = request.form['isbn_give']
    db.books.delete_one({'isbn': isbn_receive})
    return jsonify({'result': 'success'})


@app.route('/booksave', methods=['GET'])
def read_books():
    # 1. mongodb에서 모든 데이터 조회해오기 (read)
    result = list(db.books.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'books':result})


@app.route('/bookadd4')
def bookAdd4():
    return render_template('bookAdd4.html')



# @app.route('/print')
# def list_num():
#     i = 0
#     if i<=db.books.count():
#         print(i)
#         i=i+1
#     else:
#         i=0
#         print(i)
#     return render_template('main.html', i=i)
#
#
# schedule.every(1).day.at("00:00").do(list_num)



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)


