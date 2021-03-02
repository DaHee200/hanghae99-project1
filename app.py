from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

app = Flask(__name__)


## HTML을 주는 부분
@app.route('/')
def main():
    name = "sparta"
    return render_template("mainPg.html", name=name)


@app.route('/detail01')
def detail01():
    return render_template("detail01.html")


@app.route('/detail02')
def detail02():
    r = requests.get('http://openapi.seoul.go.kr:8088/6d4d776b466c656533356a4b4b5872/json/RealtimeCityAir/1/99')
    response = r.json()
    rows = response['RealtimeCityAir']['row']
    return render_template("detail02.html", rows=rows, response=response)


@app.route('/detail03')
def detail03():
    return render_template("detail03.html")


@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/Detail02', methods=['GET'])
def listing():
    videos = list(db.videos.find({}, {'_id': False}))
    return jsonify({'all_videos': videos})

## API 역할을 하는 부분
@app.route('/Detail02', methods=['POST'])
def Detail02():
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    title = soup.select_one('meta[property="og:title"]')['content']
    image = soup.select_one('meta[property="og:image"]')['content']
    desc = soup.select_one('meta[property="og:description"]')['content']

    doc = {
        'title': title,
        'image': image,
        'desc': desc,
        'url': url_receive,
        'comment': comment_receive
    }
    db.videos.insert_one(doc)

    return jsonify({'msg': '저장이 완료되었습니다'})
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

    ## API 역할을 하는 부분
