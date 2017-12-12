#!/usr/local/bin/python3
import sys
from flask import Flask
from flask_restful import Api, Resource
from flask_restful import reqparse
from regserver import regServer
import my_errors
my_errors.make_classes(my_errors.errors)

# ----- Init -----
app = Flask(__name__)
api = Api(app, errors=my_errors.errors)

# ----- reg -----


class regApi(Resource):
    def __init__(self):
        global rServer
        self.regServer = rServer
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'callback', type=str, location='json')
        self.reqparse.add_argument(
            'type', type=str, location='json')
        super(regApi, self).__init__()

    def get(self):
        print("querying reg")
        args = self.reqparse.parse_args()
        return {'reged': self.regServer.get_reg_status(**args)}

    def post(self):
        print("aquireing new reg")
        args = self.reqparse.parse_args()
        return {'reged': self.regServer.reg_service(**args)}

    def delete(self):
        print("removing reg")
        args = self.reqparse.parse_args()
        return {'unreged': self.regServer.unreg_service(**args)}


api.add_resource(regApi, '/reg', endpoint='reg')

# ----- Main -----
if __name__ == '__main__':
    port = 8083
    if len(sys.argv) > 1:
        print("taking args")
        port = int(sys.argv[1])
    lServer = regServer()
    app.run(host='0.0.0.0', debug=True, port=port)
