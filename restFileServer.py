#!/usr/local/bin/python3
# general
import sys
# flask
from flask import Flask
from flask_restful import Api, Resource, reqparse, marshal
# classes
from fileserver import fileServer
# my utils
import my_errors
my_errors.make_classes(my_errors.errors)
import my_fields

# ----- Init -----
app = Flask(__name__)
api = Api(app, errors=my_errors.errors)


class FilesListApi(Resource):
    """
    Provides API to list files on file server (ls)
    """

    def __init__(self):
        global fileS
        self.fileS = fileS
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('token', type=str, location='json')
        self.reqparse.add_argument('message', type=str, location='json')
        super(FilesListApi, self).__init__()

    def get(self):
        """Returns a list of all files on server"""
        # print("getting all files")
        args = self.reqparse.parse_args()
        return {'message': self.fileS.get_all_files(**args)}

    def delete(self):
        """TESTING ONLY! Delete the fileserver."""
        # called to delete the fileserver, testing only
        # print("unregistering all")
        self.fileS.del_all_files()


api.add_resource(FilesListApi, '/files', endpoint='files')


class FileApi(Resource):
    """
    Provides API to interact with individual files on the file server
    """

    def __init__(self):
        global fileS
        self.fileS = fileS
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('token', type=str, location='json')
        self.reqparse.add_argument('message', type=str, location='json')
        super(FileApi, self).__init__()

    def get(self):
        """Retrieve all information on a specific file, including contents"""
        # print("getting file")
        args = self.reqparse.parse_args()
        return {'message': self.fileS.get_file(**args)}

    def post(self):
        """Add a new file to the file server"""
        # print('in post file')
        args = self.reqparse.parse_args()
        return {'message': self.fileS.add_file(**args)}

    def put(self):
        """Edit/update a file already on the file server"""
        # print("editing file")
        args = self.reqparse.parse_args()
        return {'message': self.fileS.update_file(**args)}

    def delete(self):
        """Delete an individual file from the file server"""
        # print("deleting file")
        args = self.reqparse.parse_args()
        return {'message': self.fileS.del_file(**args)}


api.add_resource(FileApi, '/file', endpoint='file')


class CallbackApi(Resource):
    """
    Provides callback functionality to check if the server is up
    """

    def __init__(self):
        super(CallbackApi, self).__init__()

    def get(self):
        print("callback")
        return {'alive': True}


api.add_resource(CallbackApi, '/callback', endpoint='callback')

# ----- Main -----
if __name__ == '__main__':
    port = 8080
    if len(sys.argv) > 1:
        print("taking args")
        port = int(sys.argv[1])
    with fileServer(port) as fileS:
        if fileS.machine_id is None:
            print("no machine id")
            # sys.exit
        app.run(host='0.0.0.0', debug=True, port=port)
        print('just chilling')
