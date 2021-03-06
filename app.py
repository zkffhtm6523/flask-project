import logging
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)

# app.config['MONGO_DBNAME'] = 'restdb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/flask_mongo'

mongo = PyMongo(app)

# 테이블은 아래에 insert 때 생성됨
restapi = mongo.db.stars
star_data = {
    "name": "test10",
    "distance": "1234"
}
# restapi.insert_one(star_data)


@app.route('/star', methods=['GET'])
def get_all_stars():
    # 테이블을 가져온다.
    star = mongo.db.stars
    output = []
    for s in star.find():
        output.append({'name': s['name'], 'distance': s['distance']})
    return jsonify({'result': output})


@app.route('/star/', methods=['GET'])
def get_one_star(name):
    print('Come on')
    star = mongo.db.stars
    s = star.find_one({'name': name})
    print('dddd')
    if s:
        output = {'name': s['name'], 'distance': s['distance']}
    else:
        output = "No such name"
    return jsonify({'result': output})


@app.route('/star', methods=['POST'])
def add_star():
    star = mongo.db.stars
    name = request.json['name']
    distance = request.json['distance']
    star_id = star.insert({'name': name, 'distance': distance})
    new_star = star.find_one({'_id': star_id})
    output = {'name': new_star['name'], 'distance': new_star['distance']}
    return jsonify({'result': output})


if __name__ == '__main__':
    app.run(debug=True)
