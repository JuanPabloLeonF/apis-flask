from flask import jsonify
from configuration import db
import json
from models import User
from dto import UserDto, ResponseError
from json import JSONDecodeError


class UserRepository():

    @staticmethod
    def getAll():
        try:
            users = User.query.all()
            user_list = [UserDto.serialize(user) for user in users]
            return jsonify(user_list), 200
        except Exception as e:
            error_response = ResponseError(statusCode=500, status='error', error=str(e))
            return jsonify(error_response.serialize()), 500

    @staticmethod
    def getById(id):
        try:
            user = User.query.get(id)
            if user:
                return jsonify(UserDto.serialize(user)), 200
            else:
                error_response = ResponseError(statusCode=404, status='error', error='Usuario no encontrado')
                return jsonify(error_response.serialize()), 404
        except Exception as e:
            error_response = ResponseError(statusCode=500, status='error', error=str(e))
            return jsonify(error_response.serialize()), 500

    @staticmethod
    def create(user_data):
        try:
            user = json.loads(user_data)
            new_user = User(
                username=user.get('username'),
                email=user.get('email')
            )
            db.session.add(new_user)
            db.session.commit()

            return jsonify(UserDto.serialize(new_user)), 201
        except Exception as e:
            db.session.rollback()
            error_response = ResponseError(statusCode=500, status='error', error=str(e))
            return jsonify(error_response.serialize()), 500

    @staticmethod
    def updateById(userData, id):
        try:
            userDataJson = json.loads(userData)
            userGet = User.query.get(id)

            if userGet:
                userGet.username = userDataJson.get('username', userGet.username)
                userGet.email = userDataJson.get('email', userGet.email)
                db.session.commit()
                return jsonify(UserDto.serialize(userGet)), 200
            else:
                error_response = ResponseError(statusCode=404, status='NOT FOUND', error=f'User with id {id} not found')
                return jsonify(error_response.serialize()), 404
        except JSONDecodeError:
            error_response = ResponseError(statusCode=400, status='BAD REQUEST', error='Invalid JSON format')
            return jsonify(error_response.serialize()), 400
        except Exception as e:
            error_response = ResponseError(statusCode=500, status='INTERNAL SERVER ERROR', error=str(e))
            return jsonify(error_response.serialize()), 500

    @staticmethod
    def deleteById(id):
        try:
            userToDelete = User.query.get(id)
            if userToDelete:
                db.session.delete(userToDelete)
                db.session.commit()
                return jsonify({'message': 'User deleted successfully'}), 200
            else:
                error_response = ResponseError(statusCode=404, status='NOT FOUND', error=f'User with id {id} not found')
                return jsonify(error_response.serialize()), 404
        except Exception as e:
            error_response = ResponseError(statusCode=500, status='INTERNAL SERVER ERROR', error=str(e))
            return jsonify(error_response.serialize()), 500

