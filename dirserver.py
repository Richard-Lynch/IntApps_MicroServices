#!/usr/local/bin/python3
from flask_restful import marshal
import my_errors
my_errors.make_classes(my_errors.errors)
import my_fields
import check
# --- security ---
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# --- mongo ----
from pymongo import MongoClient
from bson.objectid import ObjectId
import mongo_stuff
import decrypt_message
import send_securily
from pprint import pprint


class dirServer():
    def __init__(self,
                 secret_key='the quick brown fox jumps over the lazy dog'):
        self.load_machines()
        self.load_files()
        self.s = Serializer(secret_key)

    # util functions
    def load_machines(self):
        self.db_machines = MongoClient().test_database.db.machines
        # drop db for testing, will not be in deployed version
        self.db_machines.drop()
        # print(self.db_machines)
        return True

    def load_files(self):
        self.db_files = MongoClient().test_database.db.machine_files
        # drop db for testing, will not be in deployed version
        self.db_files.drop()
        # print(self.db_files)
        return True

    # registration
    @check.reqs(['name', 'machine_id', 'uri'])
    def register_file(self, **kwargs):
        # print('in reg')
        # reg file, add every keyword arg (filtered by api)
        f = {k: v for k, v in kwargs.items()}
        Id = mongo_stuff.insert(self.db_files, f)
        return self.get_file(Id)

    @check.reqs(['callback'])
    def register_machine(self, **kwargs):
        m = {k: v for k, v in kwargs.items()}
        r = mongo_stuff.insert_or_override(self.db_machines, m)
        # print('registered', r)
        return r

    @check.reqs(['_id'])
    def unreg_file(self, *args, **kwargs):
        # print('in unreg file')
        kwargs['_id'] = ObjectId(kwargs['_id'])
        return bool(self.db_files.delete_one(kwargs).deleted_count)

    @check.reqs(['machine_id'])
    def unreg_machine(self, machine_id):
        # print('in unreg machine')
        self.db_files.delete_many({'machine_id': machine_id})
        return bool(
            self.db_machines.delete_many({
                '_id': ObjectId(machine_id)
            }).deleted_count)

    def get_file(self, Id):
        # print('in get file')
        f = self.db_files.find_one({'_id': ObjectId(Id)})
        if f:
            return f
        else:
            raise my_errors.not_found

    def get_machine(self, Id):
        # print('in get machine')
        m = self.db_machines.find_one({'_id': ObjectId(Id)})
        if m:
            return m
        else:
            raise my_errors.not_found

    @send_securily.with_token
    @decrypt_message.with_token
    @check.reqs(['name'])
    def search_filename(self, *args, **kwargs):
        # print('in search')
        # search via name, returns list
        files = self.db_files.find(kwargs)
        if files:
            _files = [f for f in files]
            return {
                'files':
                [marshal(f, my_fields.dir_file_fields) for f in _files]
            }

        else:
            # print("file name not found")
            raise my_errors.not_found
