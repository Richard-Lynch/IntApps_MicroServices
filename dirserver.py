#!/usr/local/bin/python3
# general
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
# --- mongo ----
from pymongo import MongoClient
from bson.objectid import ObjectId
import mongo_stuff


class dirServer():
    """
    Server providing file locations to clients
    """

    def __init__(self,
                 secret_key='the quick brown fox jumps over the lazy dog'):
        self.load_machines()
        self.load_files()
        self.s = Serializer(secret_key)

    # util functions
    def load_machines(self):
        """Load persistnet storage of registered machines"""
        self.db_machines = MongoClient().test_database.db.machines
        # drop db for testing, will not be in deployed version
        self.db_machines.drop()
        # print(self.db_machines)
        return True

    def load_files(self):
        """Load persistnet storage of registered files"""
        self.db_files = MongoClient().test_database.db.machine_files
        # drop db for testing, will not be in deployed version
        self.db_files.drop()
        # print(self.db_files)
        return True

    # registration
    @check.reqs(['name', 'machine_id', 'uri'])
    def register_file(self, **kwargs):
        """Register a new files locations"""
        # print('in reg')
        f = {k: v for k, v in kwargs.items()}
        Id = mongo_stuff.insert(self.db_files, f)
        return self.get_file(Id)

    @check.reqs(['callback'])
    def register_machine(self, **kwargs):
        """Register a new machine"""
        m = {k: v for k, v in kwargs.items()}
        r = mongo_stuff.insert_or_override(self.db_machines, m)
        return r

    @check.reqs(['_id'])
    def unreg_file(self, *args, **kwargs):
        """Unregester a file (delete its location)"""
        # print('in unreg file')
        kwargs['_id'] = ObjectId(kwargs['_id'])
        return bool(self.db_files.delete_one(kwargs).deleted_count)

    @check.reqs(['machine_id'])
    def unreg_machine(self, machine_id):
        """Unregsiter a machine (delete all its files)"""
        # print('in unreg machine')
        self.db_files.delete_many({'machine_id': machine_id})
        return bool(
            self.db_machines.delete_many({
                '_id': ObjectId(machine_id)
            }).deleted_count)

    def get_file(self, Id):
        """Retreive the location of a file by file _id"""
        # print('in get file')
        f = self.db_files.find_one({'_id': ObjectId(Id)})
        if f:
            return f
        else:
            raise my_errors.not_found

    def get_machine(self, Id):
        """Retreive machine information by machine _id"""
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
        """Search for file by name, and return list of matching files"""
        # print('in search')
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
