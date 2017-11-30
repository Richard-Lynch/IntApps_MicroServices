#!/usr/local/bin/python3
import requests
# import sys
# from flask_kerberos import requires_authentication
from flask_restful import marshal
# from collections import defaultdict
import my_errors
my_errors.make_classes(my_errors.errors)
import my_fields
import check
# --- mongo ----
from pymongo import MongoClient
# from pprint import pprint
from bson.objectid import ObjectId
import mongo_stuff


class fileServer():
    def __init__(self, port):
        # main
        self.machine_id = None
        self.load_files()
        self.dirServerAdd = "http://127.0.0.1:8081/dirs"
        self.port = port
        self.register_machine()
        self.register_initial_files()
        print("file server started")

    def __enter__(self):
        print("using fileServer as open")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("exiting")
        self.un_register_all_files()

# util functions

    def register_machine(self):
        r = requests.post(
            self.dirServerAdd + '/register',
            json=dict(
                marshal({
                    'callback':
                    'http://127.0.0.1:' + str(self.port) + '/callback',
                }, my_fields.register_machine_fields))).json()
        print(r)
        if 'machine' in r:
            self.machine_id = r['machine'].get('_id', -1)
        else:
            self.machine_id = '1'
            print('issue')
            # raise my_errors.bad_request
        return True

    def load_files(self):
        # mongo
        self.db_files = MongoClient().test_database.db.files
        # drop db for testing, will not be in deployed version
        self.db_files.drop()
        print(self.db_files)
        return True

    def del_all_files(self):
        # for testing only, would not be live
        self.db_files.drop()
        self.un_register_all_files()

# register

    def register_initial_files(self):
        for f in self.get_all_files():
            r = self.register_file(f)
            # should check here if r is correct/valid
            print(r)

    def register_file(self, Id):
        # TODO clean this up;
        # errors should be more clear
        # if/try should make more sense

        # regsiter the file with the dir server
        try:
            f = self.db_files.find_one({'_id': Id})
            r = requests.put(
                self.dirServerAdd + '/register',
                json=dict(marshal(f, my_fields.register_fields))).json()
            print('r', r)
            if 'file' in r:
                reg_uri = r['file']['reg_uri']
                self.db_files.update_one({
                    '_id': ObjectId(Id)
                }, {
                    '$set': {
                        'reg_uri': reg_uri
                    }
                })
            else:
                raise my_errors.bad_request
        except Exception:
            raise my_errors.bad_request

    def un_register_file(self, Id):
        # unregister with the dir server
        f = self.get_file(Id)
        # return the response from the request
        return requests.delete(f['reg_uri']).json()

    def un_register_all_files(self):
        # for when a machine is going down
        print("in all")
        r = requests.delete(
            self.dirServerAdd + '/register',
            json={
                'machine_id': self.machine_id
            }).json()
        print(r)

# file edits

    @check.reqs(['name', 'content'])
    def add_file(self, **kwargs):
        # example of file doc stored in mongo:
        # {
        #     '_id': 'abc123',
        #     'name': 'example.txt',
        #     'content': 'hello world',
        #     'machine_id': '2',
        #     'reg_uri': '127.0.0.1:8081/dirs/123',
        # }
        #
        # add every keyword arg (filtered by api)
        f = {k: v for k, v in kwargs.items()}
        f['machine_id'] = self.machine_id
        Id = mongo_stuff.insert(self.db_files, f)
        self.register_file(Id)
        return self.get_file(Id)

    def update_file(self, args, Id):
        # filter the args, if none dont set
        kwargs = {k: v for k, v in args.items() if v}
        # update a file on the fileserver
        return self.db_files.find_one_and_update({
            '_id': ObjectId(Id)
        }, {
            '$set': kwargs
        })
        # return self.get_file(Id)

    def del_file(self, Id):
        # delete a file from the server
        self.un_register(Id)
        return bool(
            self.db_files.delete_one({
                '_id': ObjectId(Id)
            }).deleted_count)


# return files

    def get_file(self, Id):
        f = self.db_files.find_one({'_id': ObjectId(Id)})
        if f:
            return f
        else:
            raise my_errors.not_found

    def get_all_files(self):
        # return a list of values
        return [f for f in self.db_files.find()]
