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


@auth.error_handler
def auth_error():
    raise my_errors.unauthorized


@auth.verify_password
def ver_pass(username, password):
    global aServer
    g.user_data = aServer.verify_user(username, password)
    return True


# ----- Auth -----


class AuthApi(Resource):
    def __init__(self):
        global aServer
        self.authServer = aServer
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('message', type=str, location='json')
        self.reqparse.add_argument('token', type=str, location='json')
        super(AuthApi, self).__init__()

    def get(self):
        print("checking auth")
        args = self.reqparse.parse_args()
        return {'message': self.authServer.get_auth_level(**args)}

    def post(self):
        print('in post')
        args = self.reqparse.parse_args()
        return {'message': self.authServer.create_user(**args)}

    def put(self):
        print('in put')
        args = self.reqparse.parse_args()
        return {'message': self.authServer.generate_token(**args)}


api.add_resource(AuthApi, '/auth', endpoint='auth')

# ----- Main -----
if __name__ == '__main__':
    port = 8083
    if len(sys.argv) > 1:
        print("taking args")
        port = int(sys.argv[1])
    aServer = authServer()
    app.run(host='0.0.0.0', debug=True, port=port)
