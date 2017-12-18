#!/usr/local/bin/python3
# general
import sys
# flask
from flask import Flask
from flask_restful import Api, Resource, reqparse
# classes
from aserver import authServer
# my utils
import my_errors
my_errors.make_classes(my_errors.errors)
import my_fields

# ----- Init -----
app = Flask(__name__)
api = Api(app, errors=my_errors.errors)


class AuthApi(Resource):
    """
    Provides API to authorize clients/servers using 3 key mutual authenticaion
    """

    def __init__(self):
        global aServer
        self.authServer = aServer
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('message', type=str, location='json')
        self.reqparse.add_argument('token', type=str, location='json')
        super(AuthApi, self).__init__()

    def get(self):
        """Check you authorization level"""
        # print("checking auth")
        args = self.reqparse.parse_args()
        return {'message': self.authServer.get_auth_level(**args)}

    def post(self):
        """Create a new user. Requires admin."""
        # print('in post')
        args = self.reqparse.parse_args()
        return {'message': self.authServer.create_user(**args)}

    def put(self):
        """Generate a new token with your credentials"""
        # print('in put')
        args = self.reqparse.parse_args()
        return {'message': self.authServer.generate_token(**args)}


api.add_resource(AuthApi, '/auth', endpoint='auth')

# ----- Main -----
if __name__ == '__main__':
    port = 8083
    if len(sys.argv) > 1:
        # print("taking args")
        port = int(sys.argv[1])
    aServer = authServer()
    app.run(host='0.0.0.0', debug=True, port=port)
