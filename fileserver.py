#!/usr/local/bin/python3
# general
import requests
from pprint import pprint
# flask
from flask_restful import marshal
# my utils
import my_errors
my_errors.make_classes(my_errors.errors)
import my_fields
import check
# --- security ---
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import decrypt_message
import send_securily
# --- mongo ---
from pymongo import MongoClient, ReturnDocument
from bson.objectid import ObjectId
import mongo_stuff


class fileServer():
    """
    Server providing file storage and retrieval to clients
    """

    def __init__(self,
                 port,
                 secret_key='the quick brown fox jumps over the lazy dog'):
        self.s = Serializer(secret_key)
        self.machine_id = None
        self.load_files()
        self.dirServerAdd = "http://127.0.0.1:8081/dirs"
        self.port = port
        self.register_machine()
        self.register_initial_files()
        # print("file server started")

    def __enter__(self):
        # print("using fileServer as open")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # print("exiting")
        self.un_register_all_files()

# util functions

    def load_files(self):
        """Load persistent storage of files"""
        self.db_files = MongoClient().test_database.db.files
        # drop db for testing, will not be in deployed version
        self.db_files.drop()
        print(self.db_files)
        return True

    def del_all_files(self):
        """TESTING ONLY:Delete all files on the file server"""
        # for testing only, would not be live
        self.db_files.drop()
        self.un_register_all_files()

# register

    def register_machine(self):
        """Register this file server with the directory server"""
        r = requests.get(
            self.dirServerAdd + '/register',
            json=dict(
                marshal({
                    'callback':
                    'http://127.0.0.1:' + str(self.port) + '/callback',
                }, my_fields.register_machine_fields))).json()
        # print(r)
        if 'machine' in r:
            self.machine_id = r['machine'].get('_id', -1)
            return True
        else:
            self.machine_id = '-1'
            # print('issue')
            return False

    def register_initial_files(self):
        """Register all of the files which were loaded on startup with the dir server"""
        for f in [f for f in self.db_files.find()]:
            r = self.register_file(f)
            # should check here if r is correct/valid
            print(r)

    def register_file(self, Id):
        """Register an individual file with the dir server"""
        # print('in regsiter')
        try:
            r = requests.post(
                self.dirServerAdd + '/register',
                json=dict(
                    marshal(
                        self.db_files.find_one({
                            '_id': Id
                        }), my_fields.register_fields))).json()
            self.db_files.update_one({
                '_id': ObjectId(Id)
            }, {
                '$set': {
                    'reg_uri': r['file']['reg_uri'],
                    'reg_id': r['file']['reg_id']
                }
            })
            return r
        except Exception:
            raise my_errors.bad_request

    def un_register_file(self, Id):
        """Unregsiter an individual file with the dir server"""
        # print('in unreg file')
        f = self.db_files.find_one({'_id': ObjectId(Id)})
        if f:
            return requests.put(f['reg_uri'], json={'_id': f['reg_id']}).json()
        else:
            raise my_errors.not_found

    def un_register_all_files(self):
        """Unregister all files with the dir server"""
        # print("in unreg all")
        r = requests.delete(
            self.dirServerAdd + '/register',
            json={
                'machine_id': self.machine_id
            }).json()


# file edits

    @send_securily.with_token
    @decrypt_message.with_token
    @check.reqs(['name', 'content'])
    def add_file(self, *args, **kwargs):
        """Add a file to the file server"""
        # print('in add file')
        f = {k: v for k, v in kwargs.items()}
        f['machine_id'] = self.machine_id
        Id = mongo_stuff.insert(self.db_files, f)
        self.register_file(Id)
        f = self.db_files.find_one_and_update(
            {
                '_id': ObjectId(Id)
            },
            {'$set': {
                'version': 1
            }},
            return_document=ReturnDocument.AFTER,
        )
        return {"file": marshal(f, my_fields.file_fields)}

    @send_securily.with_token
    @decrypt_message.with_token
    @check.reqs(['name', 'content', '_id', 'version'])
    def update_file(self, **kwargs):
        """Update an exisiting file in the file server"""
        # print('in update file')
        Id = kwargs['_id']
        version = kwargs['version']
        exclude = ['_id', 'version']
        kw = {
            k: v
            for k, v in kwargs.items() if v is not None and k not in exclude
        }
        f = self.db_files.find_one_and_update(
            {
                '_id': ObjectId(Id),
                'version': {
                    '$lte': version
                }
            },
            {'$set': kw,
             '$inc': {
                 'version': 1
             }},
            return_document=ReturnDocument.AFTER,
        )
        if f is None:
            raise my_errors.bad_request
        return {"file": marshal(f, my_fields.file_summary_fields)}

    @send_securily.with_token
    @decrypt_message.with_token
    @check.reqs(['_id'])
    def del_file(self, **kwargs):
        """Delete an exisiting file from the file server"""
        # print('in del file')
        Id = kwargs.get('_id')
        unreged = self.un_register_file(Id)
        return {
            'deleted':
            bool(
                self.db_files.delete_one({
                    '_id': ObjectId(Id)
                }).deleted_count)
        }

    @send_securily.with_token
    @decrypt_message.with_token
    @check.reqs(['_id'])
    def get_file(self, *args, **kwargs):
        """Retrieve an exisiting file from the file server"""
        # print('in get file')
        f = self.db_files.find_one({'_id': ObjectId(kwargs['_id'])})
        if f:
            return {'file': marshal(f, my_fields.file_fields)}
        else:
            raise my_errors.not_found

    @send_securily.with_token
    @decrypt_message.with_token
    def get_all_files(self):
        """Returns a list of all files on file server"""
        # print('in get all files')
        files = [f for f in self.db_files.find()]
        return {
            'files':
            [marshal(f, my_fields.file_summary_fields) for f in files]
        }
