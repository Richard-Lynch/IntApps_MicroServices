#!/usr/local/bin/python3

import sys
from flask import Flask, jsonify, request, make_response, url_for, g
from flask_kerberos import requires_authentication
from flask_restful import Api, Resource, abort, HTTPException
from flask_restful import reqparse, fields, marshal
# from lockserver import lockServer
from flask_httpauth import HTTPBasicAuth
from aserver import authServer
import my_errors
my_errors.make_classes(my_errors.errors)
import my_fields
import check
import decrypt_message

# ----- Init -----
app = Flask(__name__)
api = Api(app, errors=my_errors.errors)
# --- mongo ----
from pymongo import MongoClient
from bson.objectid import ObjectId
import mongo_stuff
# --- security --
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)


class demo_tokenApi(Resource):
    def __init__(self):
        global dServer
        self.demoServer = dServer
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('token', type=str, location='json')
        self.reqparse.add_argument('message', type=str, location='json')
        super(demo_tokenApi, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        # token = args.get('token')
        return {'printed': self.demoServer.print_message(**args)}


api.add_resource(demo_tokenApi, '/token', endpoint='token')


def decrypt_message_with_token(f):
    def wrapped_f(self, **kwargs):
        token = kwargs.get('token')
        message = kwargs.get('message')
        try:
            # TODO not using anything except key and timeout for now, but
            # could have other info in the token like permissions etc
            data = self.s.loads(token)
            # key = data['key']
            s = Serializer(data['key'])
            decoded_message = s.loads(message)
            return f(self, **decoded_message)
        except SignatureExpired:
            print('exp')
            # TODO change to sigexpired
            raise my_errors.unauthorized
        except BadSignature:
            print('bad')
            # TODO change to badsig
            raise my_errors.unauthorized
        except Exception as e:
            # TODO change to unknown exception
            print('e', e)
            raise my_errors.bad_request

    return wrapped_f


class demo_token_user():
    """docstring for demo_token_user"""

    def __init__(self,
                 secret_key='the quick brown fox jumps over the lazy dog'):
        self.s = Serializer(secret_key)

    @decrypt_message.with_token
    @check.reqs(['name'])
    def print_message(self, **kwargs):
        print('in print!')
        print(kwargs)
        for k, v in kwargs.items():
            print('{}: {}'.format(k, v))
        return True


if __name__ == '__main__':
    port = 8085
    if len(sys.argv) > 1:
        print("taking args")
        port = int(sys.argv[1])
    dServer = demo_token_user()
    app.run(host='0.0.0.0', debug=True, port=port)
