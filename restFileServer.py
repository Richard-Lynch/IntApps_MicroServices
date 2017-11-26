#!/usr/local/bin/python3
import sys
from flask import Flask, make_response, url_for
from flask_kerberos import requires_authentication
from flask_restful import Api, Resource, abort, HTTPException
from flask_restful import reqparse, fields, marshal
import requests
# from my_errors import errors, make_classes
import my_errors
my_errors.make_classes(my_errors.errors)
# from my_fields import *
import my_fields
from fileserver import fileServer
# ----- Files DB -----

# ----- Init -----
app = Flask(__name__)
api = Api(app, errors=my_errors.errors)

# ----- Files List -----
class FilesListApi(Resource):
    def __init__(self):
        global fileS
        self.fileS = fileS
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, location='json', required=True, help="No filename provided")
        self.reqparse.add_argument('content', type=str, location='json', default="")
        super(FilesListApi, self).__init__()
    def get(self):
        print ("getting all files")
        files = self.fileS.get_all_files()
        return { 'files' : [ marshal(files[f], my_fields.file_summary_fields) for f in files ] }
    def post(self):
        print ("adding file")
        args = self.reqparse.parse_args()
        f = self.fileS.add_file(args)
        if f == None:
            raise my_errors.file_exists
        return { "file" : marshal(f, my_fields.file_fields)}
api.add_resource(FilesListApi, '/files', endpoint = 'files')

# ----- Individual File -----
class FileApi(Resource):
    def __init__(self):
        global fileS
        self.fileS = fileS
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type = str, location = 'json')
        self.reqparse.add_argument('content', type = str, location = 'json')
        super(FileApi, self).__init__()
    def get(self, id):
        print ("getting file")
        f = self.fileS.get_file(id)
        if f == None:
            raise my_errors.not_found
        return { 'file': marshal(f, my_fields.file_fields) }
    def put(self, id):
        print ("editing file")
        args = self.reqparse.parse_args()
        f = self.fileS.update_file(args, id)
        if f == None:
            raise my_errors.not_found
        return {"file" : marshal(f, my_fields.file_summary_fields)}
    def delete (self, id):
        print ("deleting file")
        deleted = self.filesS.del_file(id)
        if deleted == None:
            raise my_errors.not_found
        return { 'deleted' : True }
api.add_resource(FileApi, '/files/<int:id>', endpoint = 'file')

# ----- Main -----
if __name__ == '__main__':
    port = 8080
    if len(sys.argv) > 1:
        print("taking args")
        port = int(sys.argv[1])
    fileS = fileServer()
    if fileS.machine_id == None:
        sys.exit
    app.run(host='0.0.0.0', debug=True, port=port)

