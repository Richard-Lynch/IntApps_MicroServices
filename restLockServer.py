#!/usr/local/bin/python3
import sys
from flask import Flask, jsonify, request, make_response, url_for
from flask_kerberos import requires_authentication
from flask_restful import Api, Resource, abort, HTTPException
from flask_restful import reqparse, fields, marshal
from lockserver import lockServer
import my_errors
my_errors.make_classes(my_errors.errors)
import my_fields
# ----- Files DB -----

# ----- Init -----
app = Flask(__name__)
api = Api(app, errors=my_errors.errors)

        

# ----- Files List -----
class FilesListApi(Resource):
    def __init__(self):
        global lServer
        self.lockServer = lServer
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('uri', type = str, location = 'json', help = "No filename provided")
        super(FilesListApi, self).__init__()

    def get(self):
        print ("checking lock")
        args = self.reqparse.parse_args()
        return { 'locked' : self.lockServer.get_lock_status(**args) }

    def post(self):
        print ("aquireing new lock")
        args = self.reqparse.parse_args()
        return { 'locked' : self.lockServer.lock_file(**args) }

    def delete(self):
        print ("removing lock")
        args = self.reqparse.parse_args()
        return { 'unlocked' : self.lockServer.unlock_file(**args) }

api.add_resource(FilesListApi, '/lock', endpoint = 'lock')

# ----- Main -----
if __name__ == '__main__':
    port = 8083
    if len(sys.argv) > 1:
        print("taking args")
        port = int(sys.argv[1])
    lServer = lockServer()
    app.run(host='0.0.0.0', debug=True, port=port)

