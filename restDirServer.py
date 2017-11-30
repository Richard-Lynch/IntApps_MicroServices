#!/usr/local/bin/python3
import sys
from flask import Flask
from flask_restful import Api, Resource
from flask_restful import reqparse, marshal
from dirserver import dirServer
import my_errors
my_errors.make_classes(my_errors.errors)
import my_fields
# ----- dirs DB -----

# ----- Init -----
app = Flask(__name__)
api = Api(app, errors=my_errors.errors)

# ----- Search -----


class SearchDirApi(Resource):
    def __init__(self):
        global dServer
        self.dirServer = dServer
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, location='json')
        super(SearchDirApi, self).__init__()

    def get(self):
        name = self.reqparse.parse_args().get('name')
        F = self.dirServer.search_filename(name)
        return {'files': [marshal(f, my_fields.dir_file_fields) for f in F]}


api.add_resource(SearchDirApi, '/dirs/search', endpoint='search')

# ----- Individual File -----


class FileApi(Resource):
    def __init__(self):
        global dServer
        self.dirServer = dServer
        self.reqparse = reqparse.RequestParser()
        # self.reqparse.add_argument('_id', type=str, location='json')
        super(FileApi, self).__init__()

    def delete(self, _id):
        print('unregistering file')
        r = self.dirServer.unreg_file(_id)
        return {'deleted': r}


api.add_resource(FileApi, '/dirs/<string:_id>', endpoint='file')

# ---- Register ----


class RegApi(Resource):
    def __init__(self):
        print("init")
        global dServer
        self.dirServer = dServer
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('_id', type=str, location='json')
        self.reqparse.add_argument('name', type=str, location='json')
        self.reqparse.add_argument('machine_id', type=str, location='json')
        self.reqparse.add_argument('uri', type=str, location='json')
        self.reqparse.add_argument('callback', type=str, location='json')
        super(RegApi, self).__init__()

    def post(self):
        print("registering new machine")
        args = self.reqparse.parse_args()
        return {
            "machine":
            marshal(
                self.dirServer.register_machine(**args),
                my_fields.registered_machine_fields)
        }

    def put(self):
        print("registering new file")
        args = self.reqparse.parse_args()
        # add the file to the dir server
        # return the file reg summary
        return {
            "file":
            marshal(
                self.dirServer.register_file(**args),
                my_fields.registered_fields)
        }

    def delete(self):
        print('unregistering machine')
        args = self.reqparse.parse_args()
        # unregister the machine
        # return the machine_id
        return {"un_reged": self.dirServer.unreg_machine(**args)}


api.add_resource(RegApi, '/dirs/register', endpoint='register')

# ----- Main -----
if __name__ == '__main__':
    port = 8081
    if len(sys.argv) > 1:
        print("taking args")
        port = int(sys.argv[1])
    dServer = dirServer()
    app.run(host='0.0.0.0', debug=True, port=port)
