#!/usr/local/bin/python3
import sys
from flask import Flask, jsonify, request, make_response, url_for
from flask_kerberos import requires_authentication
from flask_restful import Api, Resource, abort, HTTPException
from flask_restful import reqparse, fields, marshal
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
        self.reqparse.add_argument('name', type = str, location = 'json')
        super(SearchDirApi, self).__init__()

    def get(self):
        name = self.reqparse.parse_args().get('name')
        F = self.dirServer.search_filename(name)
        return { 'files': [marshal(f, my_fields.dir_file_fields) for f in F] }

api.add_resource(SearchDirApi, '/dirs/search', endpoint = 'search')

# ----- Individual File -----
class FileApi(Resource):
    def __init__(self):
        global dServer
        self.dirServer = dServer
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('Id', type=str, location='json')
        super(FileApi, self).__init__()

    def delete (self, Id):
        print ('unregistering file')
        f = self.dirServer.unreg_file(Id)
        return { 'deleted': marshal(f, my_fields.dir_file_fields) }

api.add_resource(FileApi, '/dirs/<int:Id>', endpoint='file')

# ---- Register ----
class RegApi(Resource):
    def __init__(self):
        print("in reg")
        global dServer
        self.dirServer = dServer
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('Id', type=str, location='json')
        self.reqparse.add_argument('name', type=str, location='json')
        self.reqparse.add_argument('machine_id', type=str, location='json')
        self.reqparse.add_argument('uri', type=str, location='json')
        super(RegApi, self).__init__()
        
    def post(self):
        print ("registering new machine")
        return { "Id" : self.dirServer.get_next_machince() }

    def put(self):
        print ("registering new file")
        # required args
        reqs = ['name', 'machine_id', 'uri']
        # read args
        args = self.reqparse.parse_args()
        # check that all required args are present
        if all (req in args for req in reqs):
            # strip any unnessasary keyvalue pairs
            kwargs = { req: args[req] for req in reqs }
            # add the file to the file server
            f = self.dirServer.register_file(**kwargs)
            # return the file summary
            return { "file" : marshal(f, my_fields.registered_fields)}
        else:
            # if not all reqs are met
            raise my_errors.bad_request

    def delete(self):
        reqs = ['machine_id']
        args = self.reqparse.parse_args()
        # check that all required args are present
        if all (req in args for req in reqs):
            # strip any unnessasary keyvalue pairs
            kwargs = { req: args[req] for req in reqs }
            # add the file to the file server
            m_id = self.dirServer.unreg_machine(**kwargs)
            # return the file summary
            return { "un_reged" : m_id}
        else:
            # if not all reqs are met
            raise my_errors.bad_request

api.add_resource(RegApi, '/dirs/register', endpoint='register')

# ----- Main -----
if __name__ == '__main__':
    port = 8081
    if len(sys.argv) > 1:
        print("taking args")
        port = int(sys.argv[1])
    dServer = dirServer()
    app.run(host='0.0.0.0', debug=True, port=port)

