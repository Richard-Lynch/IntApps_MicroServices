#!/usr/local/bin/python3
import requests
from flask_restful import marshal
import my_errors
my_errors.make_classes(my_errors.errors)
import my_fields
import check
import decrypt_message
import send_securily
from pprint import pprint
# --- security ---
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# --- mongo ---
from pymongo import MongoClient
from pymongo import ReturnDocument
from bson.objectid import ObjectId
import mongo_stuff


class fileServer():
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
        print("file server started")

    def __enter__(self):
        print("using fileServer as open")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("exiting")
        self.un_register_all_files()

# util functions

    def register_machine(self):
        r = requests.get(
            self.dirServerAdd + '/register',
            json=dict(
                marshal({
                    'callback':
                    'http://127.0.0.1:' + str(self.port) + '/callback',
                }, my_fields.register_machine_fields))).json()
        print(r)
        if 'machine' in r:
            self.machine_id = r['machine'].get('_id', -1)
            return True
        else:
            self.machine_id = '-1'
            print('issue')
            return False

    def load_files(self):
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
        for f in [f for f in self.db_files.find()]:
            r = self.register_file(f)
            # should check here if r is correct/valid
            print(r)

    def register_file(self, Id):
        # regsiter the file with the dir server
        try:
            print('in regsiter')
            f = self.db_files.find_one({'_id': Id})
            print('found file')
            print(f)
            r = requests.post(
                self.dirServerAdd + '/register',
                json=dict(marshal(f, my_fields.register_fields))).json()
            print('request')
            pprint(r)
            self.db_files.update_one({
                '_id': ObjectId(Id)
            }, {
                '$set': {
                    'reg_uri': r['file']['reg_uri'],
                    'reg_id': r['file']['reg_id']
                }
            })
            print('file updated')
            return r
        except Exception:
            raise my_errors.bad_request

    def un_register_file(self, Id):
        print('in unreg file')
        f = self.db_files.find_one({'_id': ObjectId(Id)})
        print(type(f))
        # if '_id' in f[0]:
        if f:
            print('found')
            print(f)
            return requests.put(f['reg_uri'], json={'_id': f['reg_id']}).json()
        else:
            print('not found')
            raise my_errors.not_found

    def un_register_all_files(self):
        # for when a machine is going down
        print("in unreg all")
        r = requests.delete(
            self.dirServerAdd + '/register',
            json={
                'machine_id': self.machine_id
            }).json()
        print(r)


# file edits

    @send_securily.with_token
    @decrypt_message.with_token
    @check.reqs(['name', 'content'])
    def add_file(self, *args, **kwargs):
        print('in add file')
        f = {k: v for k, v in kwargs.items()}
        f['machine_id'] = self.machine_id
        Id = mongo_stuff.insert(self.db_files, f)
        self.register_file(Id)
        print('file reged')
        print('id')
        print(Id)
        f = self.db_files.find_one_and_update(
            {
                '_id': ObjectId(Id)
            },
            {'$set': {
                'version': 1
            }},
            return_document=ReturnDocument.AFTER,
        )
        print('file')
        pprint(f)
        return {"file": marshal(f, my_fields.file_fields)}

    @send_securily.with_token
    @decrypt_message.with_token
    @check.reqs(['name', 'content', '_id', 'version'])
    def update_file(self, **kwargs):
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
        print('file')
        print(f)
        return {"file": marshal(f, my_fields.file_summary_fields)}

    @send_securily.with_token
    @decrypt_message.with_token
    @check.reqs(['_id'])
    def del_file(self, **kwargs):
        Id = kwargs.get('_id')
        unreged = self.un_register_file(Id)
        print('unr')
        print(unreged)
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
        f = self.db_files.find_one({'_id': ObjectId(kwargs['_id'])})
        if f:
            return {'file': marshal(f, my_fields.file_fields)}
        else:
            print('file not found')
            # TODO this is being caught and discarded by decrypt
            raise my_errors.not_found

    @send_securily.with_token
    @decrypt_message.with_token
    def get_all_files(self):
        # return a list of values
        files = [f for f in self.db_files.find()]
        return {
            'files':
            [marshal(f, my_fields.file_summary_fields) for f in files]
        }
