#!/usr/local/bin/python3
import sys
from flask import Flask, g
from flask_restful import Api, Resource
from flask_restful import reqparse, fields, marshal
import my_errors
my_errors.make_classes(my_errors.errors)
import my_fields
from flask_httpauth import HTTPBasicAuth
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import random
import string
# ----- Init -----
from aserver import authServer
app = Flask(__name__)
api = Api(app, errors=my_errors.errors)
auth = HTTPBasicAuth()
# this should be set up more safely, key thrown away after serializer created etc
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'


@auth.error_handler
def auth_error():
    raise my_errors.unauthorized


@auth.verify_password
def ver_pass(username, password):
    global aServer
    g.user_data = aServer.verify_user(username, password)
    return True


def key_generator(size=24, chars=(string.ascii_letters + string.digits)):
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))


# ----- Auth -----


class AuthApi(Resource):
    def __init__(self):
        global aServer
        self.authServer = aServer
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, location='json')
        self.reqparse.add_argument('password', type=str, location='json')
        self.reqparse.add_argument('hashed', type=str, location='json')
        super(AuthApi, self).__init__()

    @auth.login_required
    def get(self):
        print("checking auth")
        return {'auth': True}

    def post(self):
        print("createing new user")
        args = self.reqparse.parse_args()
        return {'created': self.authServer.create_user(**args)}

    @auth.login_required
    def put(self, expiration=600):
        # generate_auth_token
        g.user_data['_id'] = str(g.user_data['_id'])
        key = key_generator()
        g.user_data['key'] = key
        d = self.authServer.s.dumps(g.user_data).decode()
        # presuming the connection with the client is secure aka HTTPS
        return {'token': d, 'key': key}


api.add_resource(AuthApi, '/auth', endpoint='auth')

# ----- Main -----
if __name__ == '__main__':
    port = 8083
    if len(sys.argv) > 1:
        print("taking args")
        port = int(sys.argv[1])
    aServer = authServer()
    app.run(host='0.0.0.0', debug=True, port=port)
