# -*- coding:utf-8 -*-

from flask import render_template
from flask import url_for
from flask import request
from json import loads, dumps
import phpserialize as php
import time
from requests import request as fetch
from sqlalchemy.exc import *
from redis import Redis
from redis.exceptions import ConnectionError
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.sqlalchemy import *
from flask import Flask
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/qitianpeng/test.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, title, body, category, pub_date=None):
        self.title = title
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.category = category

    def __repr__(self):
        return '<Post %r>' % self.title


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name

@app.route('/')
def hello_world():
    try:
        r = Redis(host='127.0.0.1', port=6379)
        info = r.info()
    except ConnectionError:
        info = 'can\'t '
        pass
    try:
        user = User('rollingback', 'lackgod@hotmail.com')
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        pass
    return render_template('home.html', path=request.path, info=info)


@app.route('/json')
def home():
    return render_template('json.html', path=request.path)


@app.route('/prettyJson', methods=['post'])
def pretty_json():
    json_data = request.form['jsonText']
    type = request.form['type']
    try:
        json_data = loads(json_data)
        if type == 'phpSerialize':
            json_data = php.dumps(json_data)
        elif type == 'dict':
            json_data = str(json_data)
        elif type == 'pretty':
            json_data = dumps(json_data, indent=4)
        elif type == 'php':
            json_data = dumps(json_data, indent=4)
            json_data = json_data.replace('{', '[').replace('}', ']').replace(':', '=>')
    except ValueError:
        json_data = '不是json'
    return str(json_data)


@app.route('/date')
def date_format():
    return render_template('date.html', path=request.path)


@app.route('/time-parse', methods=['post'])
def time_parse():
    type = request.form['type']
    if type == 'toDate':
        timestamp = request.form['time']
        date_time = datetime.fromtimestamp(float(timestamp))
        return str(date_time)
    elif type == 'toTimestamp':
        try:
            date_time = request.form['date_time']
            date_time_obj = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
            timestamp = time.mktime(date_time_obj.timetuple())
            return str(timestamp)
        except ValueError:
            return 'error'


@app.route('/requests')
def requests():
    return render_template('requests.html', path=request.path)


@app.route('/fetch-request', methods=['post'])
def fetch_request():
    endpoint = request.form['endpoint']
    request_type = request.form['type']
    try:
        params = request.form['params']
    except KeyError:
        params = []
    try:
        header = request.form['header']
        r = fetch(request_type, endpoint, data=params, headers=header)
    except KeyError:
        r = fetch(request_type, endpoint, data=params)
    response_text = {
        'headers': unicode(r.headers),
        'status_code': unicode(r.status_code),
        'content': unicode(r.text)
    }
    return dumps(response_text)


if __name__ == '__main__':
    app.debug = True
    app.run()
