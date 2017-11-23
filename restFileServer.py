#!/usr/local/bin/python3

from flask import Flask, jsonify, request, make_response, url_for
from flask_kerberos import requires_authentication
from flask_restful import Api, Resource, abort, HTTPException
from flask_restful import reqparse, fields, marshal

# ----- Files DB -----
files = [
        {"name": "Richie", 'id' : 0, 'conent' : "sup fella!"},
        {"name": "Ali", 'id' : 1, 'conent' : "like totally omg"},
        {"name": "Jenny", 'id' : 2, 'conent' : "I run fast"},
        {"name": "Ste", 'id' : 3, 'content' : "I'm really handsome"}
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

# ----- Files List -----
class FilesListApi(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type = str, location = 'json', required = True, help = "No filename provided")
        self.reqparse.add_argument('content', type = str, location = 'json', default = "")
        super(FilesListApi, self).__init__()
    def get(self):
        return { 'files' : [ marshal(f, file_summary_fields) for f in files ] }
    def post(self):
        args = self.reqparse.parse_args()
        f = {}
        for k, v in args.items():
            f[k] = v
        f['id'] = files[-1]['id'] + 1
        files.append(f)
        return marshal(f, file_fields)
api.add_resource(FilesListApi, '/files', endpoint = 'files')

# ----- Individual File -----
class FileApi(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type = str, location = 'json')
        self.reqparse.add_argument('content', type = str, location = 'json')
        super(FileApi, self).__init__()
    def get(self, id):
        f = list(filter(lambda F: F['id'] == id, files))
        if len(f) == 0:
            raise not_found
        return { 'file': marshal(f[0], file_fields) }
    def put(self, id):
        f = list(filter(lambda F: F['id'] == id, files))
        if len(f) == 0:
            raise not_found
        f = f[0]
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v != None:
                f[k] = v
        return marshal(f, file_summary_fields)
    def delete (self, id):
        f = list(filter(lambda F: F['id'] == id, files))
        if len(f) == 0:
            raise not_found
        files.remove(f[0])
        return { 'result' : True }
api.add_resource(FileApi, '/files/<int:id>', endpoint = 'file')

# ----- Main -----
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)

