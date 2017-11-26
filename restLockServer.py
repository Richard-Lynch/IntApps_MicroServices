#!/usr/local/bin/python3
import sys
from flask import Flask, jsonify, request, make_response, url_for
from flask_kerberos import requires_authentication
from flask_restful import Api, Resource, abort, HTTPException
from flask_restful import reqparse, fields, marshal
from lockserver import lockServer
from my_errors import *
from my_fields import *
# ----- Files DB -----

# ----- Init -----
app = Flask(__name__)
api = Api(app, errors=errors)

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
        if 'uri' in args.keys():
            return { 'locked' : self.dirserver.get_lock_status(args.get(uri)) }
        else:
            raise not_found
    def post(self):
        print ("aquireing new lock")
        args = self.reqparse.parse_args()
        if 'uri' in args.keys():
            return { 'lock' : self.dirserver.lock_file(args.get(uri)) }
        else:
            raise bad_request
    def delete(self):
        print ("aquireing new lock")
        args = self.reqparse.parse_args()
        if 'uri' in args.keys():
            return { 'unlocked' : self.lockServer.unlock_file(uri) }
        else:
            raise bad_request
api.add_resource(FilesListApi, '/files', endpoint = 'files')

# ----- Main -----
if __name__ == '__main__':
    port = 8083
    if len(sys.argv) > 1:
        print("taking args")
        port = int(sys.argv[1])
    lServer = lockServer()
    app.run(host='0.0.0.0', debug=True, port=port)

