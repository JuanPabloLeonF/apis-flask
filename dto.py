class UserDto:
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

    @staticmethod
    def serialize(user):
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }

class ResponseError:
    def __init__(self, statusCode, status, error):
        self.statusCode = statusCode
        self.status = status
        self.error = error

    def serialize(self):
        return {
            'statusCode': self.statusCode,
            'status': self.status,
            'error': self.error
        }