#!/usr/local/bin/python3

from flask import Flask, jsonify, request, make_response, url_for
from flask_kerberos import requires_authentication
from flask_restful import Api, Resource, abort, HTTPException
from flask_restful import reqparse, fields, marshal
import requests
import my_errors
# ----- Files DB -----
files = [
        # {"name": "Richie", 'id' : 0, 'conent' : "sup fella!"},
        # {"name": "Ali", 'id' : 1, 'conent' : "like totally omg"},
        # {"name": "Jenny", 'id' : 2, 'conent' : "I run fast"},
        # {"name": "Ste", 'id' : 3, 'content' : "I'm really handsome"}
        ]


# ----- Init -----
app = Flask(__name__)
api = Api(app, errors=errors)

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
        files = self.fileS.get_all_files()
        return { 'files' : [ marshal(files[f], file_summary_fields) for f in files ] }
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
        self.dirServerAdd = "http://127.0.0.1:8081/files"
        r = requests.post(self.dirServerAdd).json()
        if 'id' in r:
            self.machine_id = r['id']
            self.register_initial_files()
        print ("file server started")
    def load_files(self):
        return {}
    def register_initial_files(self):
        if len (self.files) > 0:
            # F = [dict(marshal(self.files[f], register_fields)) for f in self.files] 
            # F = [dict(marshal(self.files[f], register_fields)) for f in self.files] 
            print ("F", F)
            if len(F) > 0:
                for f in F:
                    print ("f", dict(f))
                    r = requests.put(self.dirServerAdd, json=dict(f))
                    print (r.json())
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
        r = requests.put(self.dirServerAdd, json=dict(f))
        self.files[f['name']] = f
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
        return self.files
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
    import my_fields
    my_fields.init_fields(fileS.machine_id)    
    from my_fields import *
    app.run(host='0.0.0.0', debug=True, port=8080)

