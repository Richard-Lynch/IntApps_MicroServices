#!/usr/local/bin/python3
# general
import sys
# flask
from flask import Flask
from flask_restful import Api, Resource, reqparse, marshal
# classes
from dirserver import dirServer
# my utils
import my_errors
my_errors.make_classes(my_errors.errors)
import my_fields

# ----- Init -----
app = Flask(__name__)
api = Api(app, errors=my_errors.errors)


class SearchDirApi(Resource):
    """
    Provides API to search directory server files by name
    """

    def __init__(self):
        global dServer
        self.dirServer = dServer
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('message', type=str, location='json')
        self.reqparse.add_argument('token', type=str, location='json')
        super(SearchDirApi, self).__init__()

    def get(self):
        """Search for an individual file by name"""
        args = self.reqparse.parse_args()
        return {'message': self.dirServer.search_filename(**args)}


api.add_resource(SearchDirApi, '/dirs/search', endpoint='search')


class RegApi(Resource):
    """
    Provides API to regsiter files and machines with dirServer
    """

    def __init__(self):
        global dServer
        self.dirServer = dServer
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('_id', type=str, location='json')
        self.reqparse.add_argument('name', type=str, location='json')
        self.reqparse.add_argument('machine_id', type=str, location='json')
        self.reqparse.add_argument('uri', type=str, location='json')
        self.reqparse.add_argument('callback', type=str, location='json')
        super(RegApi, self).__init__()

    def get(self):
        """Register a new fileServer with the dirServer"""
        # print("registering new machine")
        args = self.reqparse.parse_args()
        return {
            "machine":
            marshal(
                self.dirServer.register_machine(**args),
                my_fields.registered_machine_fields)
        }

    def post(self):
        """Register a new file with the dirServer"""
        # print("registering new file")
        args = self.reqparse.parse_args()
        return {
            "file":
            marshal(
                self.dirServer.register_file(**args),
                my_fields.registered_fields)
        }

    def put(self):
        """Unregister (delete) a file from the dirServer"""
        # print('unregistering file')
        args = self.reqparse.parse_args()
        r = self.dirServer.unreg_file(**args)
        return {'deleted': r}

    def delete(self):
        """Unregister (delete) a machine (and files) from the dirServer"""
        # print('unregistering machine')
        args = self.reqparse.parse_args()
        return {"un_reged": self.dirServer.unreg_machine(**args)}


api.add_resource(RegApi, '/dirs/register', endpoint='register')

# ----- Main -----
if __name__ == '__main__':
    port = 8081
    if len(sys.argv) > 1:
        # print("taking args")
        port = int(sys.argv[1])
    dServer = dirServer()
    app.run(host='0.0.0.0', debug=True, port=port)
