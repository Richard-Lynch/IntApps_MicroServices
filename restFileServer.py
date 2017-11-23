#!/usr/local/bin/python3

from flask import Flask, jsonify, request, make_response, url_for
from flask_kerberos import requires_authentication
from flask_restful import Api, Resource, abort, HTTPException
from flask_restful import reqparse, fields, marshal
import requests

# ----- Files DB -----
files = [
        # {"name": "Richie", 'id' : 0, 'conent' : "sup fella!"},
        # {"name": "Ali", 'id' : 1, 'conent' : "like totally omg"},
        # {"name": "Jenny", 'id' : 2, 'conent' : "I run fast"},
        # {"name": "Ste", 'id' : 3, 'content' : "I'm really handsome"}
        ]

# ----- Errors -----
errors = {
        'not_found' : {
            'message' : "Not Found",
            'status' : 404,
            },
        'bad_request' : {
            'message' : 'Bad Request',
            'status' : 400,
            },
        'unauthorized' : {
            'message' : 'Unauthorized Acces',
            'status' : 403,
            },
        }

class not_found(HTTPException):
    code = 400
class bad_request(HTTPException):
    code = 400
class unauthorized(HTTPException):
    code = 400

# ----- Init -----
app = Flask(__name__)
api = Api(app, errors=errors)

# ----- fields -----
file_summary_fields = {
    'name': fields.String,
    'id': fields.Integer,
    'uri': fields.Url('file', absolute=True),
    'https_uri': fields.Url('file', absolute=True, scheme='https')
}
file_fields = {
    'name': fields.String,
    'id': fields.Integer,
    'uri': fields.Url('file', absolute=True),
    'https_uri': fields.Url('file', absolute=True, scheme='https'),
    'content': fields.String
}
file_list_fields={
        'files' : fields.Nested(file_fields)
    }
register_fields = {
    'name': fields.String,
    'machine_id' : fields.Integer(default=fileS.machine_id),
    'uri': fields.Url('files', absolute=True),
    }
# ----- Files List -----
class FilesListApi(Resource):
    def __init__(self):
        global fileS
        self.fileS = fileS
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type = str, location = 'json', required = True, help = "No filename provided")
        self.reqparse.add_argument('content', type = str, location = 'json', default = "")
        super(FilesListApi, self).__init__()
    def get(self):
        return { 'files' : [ marshal(f, file_summary_fields) for f in self.fileS.get_all_files() ] }
    def post(self):
        args = self.reqparse.parse_args()
        f = self.fileS.add_file(args)
        if f == None:
            return { 'error' : 'file exists' }
        return { "file" : marshal(f, file_fields)}
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
        f = self.fileS.get_file(id)
        if f == None:
            raise not_found
        return { 'file': marshal(f, file_fields) }
    def put(self, id):
        args = self.reqparse.parse_args()
        f = self.fileS.update_file(id, args)
        if f == None:
            raise not_found
        return {"file" : marshal(f, file_summary_fields)}
    def delete (self, id):
        return { 'result' : self.filesS.remove(id) }
api.add_resource(FileApi, '/files/<int:id>', endpoint = 'file')

class fileServer():
    def __init__(self):
        self.files = self.load_files()
        self.next_id = 1
        dirServerAdd = "http://127.0.0.1:8081/files"
        r = requests.post(dirServerAdd).json()
        if 'id' in r:
            self.machine_id = r['id']
            F = [ dict(marshal(f, register_fields)) for f in self.files ] 
            print ("F", F)
            if len(F) > 0:
                for f in F:
                    print ("f", dict(f))
                    r = requests.put(dirServerAdd, json=dict(f))
                    print (r.json())
        print ("file server started")
    def load_files(self):
        return {}
    def get_next(self):
        # lock
        current = self.next_id
        self.next_id += 1
        # release
        return current
    def add_file(self, args):
        f = {}
        # do any checking here
        if 'name' in args.items():
            if args.get('name') in self.files:
                return None
        for k, v in args.items():
            f[k] = v
        f['id'] = self.get_next()
        files.append(f)
        return f
    def update_file(self, args):
        f = self.fileS.get_file(id)
        if f != None:
            for k, v in args.items():
                if v != None:
                    f[k] = v
        return f
    def get_file(self, id):
        f = list(filter(lambda F: F['id'] == id, files))
        if len(f) > 0:
            return None
        else:
            return f[0]
    def get_all_files(self):
        return self.files[:]
    def del_file(self, id):
        f = self.fileS.get_file(id)
        if f == None:
            raise not_found
        if file['name'] in self.files:
            self.files.remove(file)
            return True
        return False

        

# ----- Main -----
if __name__ == '__main__':
    fileS = fileServer()
    from my_errors import *
    app.run(host='0.0.0.0', debug=True, port=8080)

