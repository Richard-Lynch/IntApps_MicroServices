#!/usr/local/bin/python3
import sys
from flask import Flask, make_response, url_for
from flask_kerberos import requires_authentication
from flask_restful import Api, Resource, abort, HTTPException
from flask_restful import reqparse, fields, marshal
import requests
import my_errors
my_errors.make_classes(my_errors.errors)
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
        self.reqparse.add_argument('name', type=str, location='json')
        self.reqparse.add_argument('content', type=str, location='json', default="")
        super(FilesListApi, self).__init__()

    def get(self):
        print ("getting all files")
        # reqs = [] 
        files = self.fileS.get_all_files()
        return { 'files' : [ marshal(f, my_fields.file_summary_fields) for f in files ] }

    def post(self):
        print ("adding file")
        # required args
        reqs = ['name', 'content']
        # read args
        args = self.reqparse.parse_args()
        # check that all required args are present
        if all (req in args for req in reqs):
            # strip any unnessasary keyvalue pairs
            kwargs = { req: args[req] for req in reqs }
            # add the file to the file server
            f = self.fileS.add_file(**kwargs)
            # return the file summary
            return { "file" : marshal(f, my_fields.file_fields)}
        else:
            # if not all reqs are met
            raise my_errors.bad_request

    def delete(self):
        # called to delete the fileserver, testing only
        print ("unregistering all")
        self.fileS.un_register_all_files()

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
        return { 'file': marshal(f, my_fields.file_fields) }

    def put(self, id):
        print ("editing file")
        args = self.reqparse.parse_args()
        f = self.fileS.update_file(args, id)
        return {"file" : marshal(f, my_fields.file_summary_fields)}

    def delete (self, id):
        print ("deleting file")
        return { 'deleted' : self.filesS.del_file(id) }

api.add_resource(FileApi, '/files/<int:id>', endpoint = 'file')

# ----- Main -----
if __name__ == '__main__':
    # default port
    port = 8080
    # if args
    if len(sys.argv) > 1:
        print("taking args")
        port = int(sys.argv[1])
    fileS = fileServer()
    if fileS.machine_id == None:
        sys.exit
    app.run(host='0.0.0.0', debug=True, port=port)

