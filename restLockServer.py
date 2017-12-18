#!/usr/local/bin/python3
# general
import sys
# flask
from flask import Flask
from flask_restful import Api, Resource, reqparse
# classes
from lockserver import lockServer
# my utils
import my_errors
my_errors.make_classes(my_errors.errors)

# ----- Init -----
app = Flask(__name__)
api = Api(app, errors=my_errors.errors)


class LockApi(Resource):
    """
    Provides API to lock file by uri and file id (_fid)
    """

    def __init__(self):
        global lServer
        self.lockServer = lServer
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('token', type=str, location='json')
        self.reqparse.add_argument('message', type=str, location='json')
        super(LockApi, self).__init__()

    def get(self):
        """Get lock status of a file"""
        # print("checking lock")
        args = self.reqparse.parse_args()
        return {'message': self.lockServer.get_lock_status(**args)}

    def post(self):
        """Lock a file"""
        # print("aquireing new lock")
        args = self.reqparse.parse_args()
        return {'message': self.lockServer.lock_file(**args)}

    def delete(self):
        """Unlock a file"""
        # print("removing lock")
        args = self.reqparse.parse_args()
        return {'message': self.lockServer.unlock_file(**args)}


api.add_resource(LockApi, '/lock', endpoint='lock')

# ----- Main -----
if __name__ == '__main__':
    port = 8084
    if len(sys.argv) > 1:
        # print("taking args")
        port = int(sys.argv[1])
    lServer = lockServer()
    app.run(host='0.0.0.0', debug=True, port=port)
