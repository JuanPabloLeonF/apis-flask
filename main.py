import os
from flask import Flask, jsonify, request
from configuration import init_app, db
from models import User
from repository import UserRepository

app = Flask(__name__)
init_app(app)

@app.route("/")
@app.route("/products")
def init():
    return f"Hello!"

@app.route('/getById/<string:id>', methods=['GET'])
def getById(id):
    return UserRepository.getById(id)

@app.route('/create', methods=['GET','POST'])
def create():
    user = request.data
    return UserRepository.create(user)

@app.route('/getAll', methods=['GET'])
def getAll(): 
    user = request.data
    return UserRepository.getAll()

@app.route('/updateById/<string:id>', methods=['PUT', 'GET'])
def updateById(id):
    user = request.data
    return UserRepository.updateById(user,id)

@app.route('/deleteById/<string:id>', methods=['DELETE', 'GET'])
def deleteById(id):
    return UserRepository.deleteById(id)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
    with app.app_context():
        db.create_all()