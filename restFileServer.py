#!/usr/local/bin/python3
import sys
from flask import Flask
from flask_restful import Api, Resource
from flask_restful import reqparse, marshal
import my_errors
my_errors.make_classes(my_errors.errors)
import my_fields
from fileserver import fileServer

# ----- Init -----
app = Flask(__name__)
api = Api(app, errors=my_errors.errors)

# ----- Files List -----


class FilesListApi(Resource):
    def __init__(self):
        global fileS
        self.fileS = fileS
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('token', type=str, location='json')
        self.reqparse.add_argument('message', type=str, location='json')
        super(FilesListApi, self).__init__()

    def get(self):
        print("getting all files")
        args = self.reqparse.parse_args()
        return {'message': self.fileS.get_all_files(**args)}

    def post(self):
        print('in post file')
        args = self.reqparse.parse_args()
        return {'message': self.fileS.add_file(**args)}

    def delete(self):
        # called to delete the fileserver, testing only
        print("unregistering all")
        self.fileS.del_all_files()


api.add_resource(FilesListApi, '/files', endpoint='files')

# ----- Individual File -----


class FileApi(Resource):
    def __init__(self):
        global fileS
        self.fileS = fileS
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('token', type=str, location='json')
        self.reqparse.add_argument('message', type=str, location='json')
        super(FileApi, self).__init__()

    def get(self):
        print("getting file")
        args = self.reqparse.parse_args()
        return {'message': self.fileS.get_file(**args)}

    def put(self):
        print("editing file")
        args = self.reqparse.parse_args()
        return {'message': self.fileS.update_file(**args)}
        # return {"file": marshal(f, my_fields.file_summary_fields)}

    def delete(self):
        print("deleting file")
        args = self.reqparse.parse_args()
        return {'message': self.fileS.del_file(**args)}


api.add_resource(FileApi, '/file', endpoint='file')


class CallbackApi(Resource):
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
