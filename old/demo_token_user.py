#!/usr/local/bin/python3

import sys
from flask import Flask, g
from flask_restful import Api, Resource
from flask_restful import reqparse
import my_errors
my_errors.make_classes(my_errors.errors)
import check
import decrypt_message

# ----- Init -----
app = Flask(__name__)
api = Api(app, errors=my_errors.errors)
# --- security --
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


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
