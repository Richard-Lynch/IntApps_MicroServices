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
        # self.reqparse.add_argument('name', type=str, location='json')
        # self.reqparse.add_argument(
        #     'content', type=str, location='json', default="")
        super(FilesListApi, self).__init__()

    def get(self):
        print("getting all files")
        files = self.fileS.get_all_files()
        return {
            'files':
            [marshal(f, my_fields.file_summary_fields) for f in files]
        }

    def post(self):
        print('in post file')
        args = self.reqparse.parse_args()
        # add the file to the file server
        # return the file summary
        return {
            "file":
            marshal(
                self.fileS.add_file(**args), my_fields.file_summary_fields)
        }

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
        # self.reqparse.add_argument('name', type=str, location='json')
        # self.reqparse.add_argument('content', type=str, location='json')
        super(FileApi, self).__init__()

    def get(self, _id):
        print("getting file")
        args = self.reqparse.parse_args()
        f = self.fileS.get_file(_id, **args)
        return {'file': marshal(f, my_fields.file_fields)}

    def put(self, _id):
        print("editing file")
        args = self.reqparse.parse_args()
        f = self.fileS.update_file(args, _id)
        return {"file": marshal(f, my_fields.file_summary_fields)}

    def delete(self, _id):
        print("deleting file")
        return {'deleted': self.filesS.del_file(_id)}


api.add_resource(FileApi, '/files/<string:_id>', endpoint='file')


class CallbackApi(Resource):
    def __init__(self):
        super(CallbackApi, self).__init__()

    def get(self):
        print("callback")
        return {'alive': True}


api.add_resource(CallbackApi, '/callback', endpoint='callback')

# ----- Main -----
if __name__ == '__main__':
    # default port
    port = 8080
    # if args
    if len(sys.argv) > 1:
        print("taking args")
        port = int(sys.argv[1])
    # fileS = fileServer()
    with fileServer(port) as fileS:
        if fileS.machine_id is None:
            print("no machine id")
            # sys.exit
        app.run(host='0.0.0.0', debug=True, port=port)
        print('just chilling')
