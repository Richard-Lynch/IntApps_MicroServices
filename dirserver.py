#!/usr/local/bin/python3
import my_errors
my_errors.make_classes(my_errors.errors)
# import my_fields
# from collections import defaultdict
import check
# --- mongo ----
from pymongo import MongoClient
# from pprint import pprint
from bson.objectid import ObjectId
import mongo_stuff


class dirServer():
    def __init__(self):
        self.load_machines()
        self.load_files()

    # util functions
    def load_machines(self):
        # mongo
        self.db_machines = MongoClient().test_database.db.machines
        # drop db for testing, will not be in deployed version
        self.db_machines.drop()
        print(self.db_machines)
        return True

    def load_files(self):
        # mongo
        self.db_files = MongoClient().test_database.db.machine_files
        # drop db for testing, will not be in deployed version
        self.db_files.drop()
        print(self.db_files)
        return True

    # registration
    @check.reqs(['name', 'machine_id', 'uri'])
    def register_file(self, **kwargs):
        # reg file, add every keyword arg (filtered by api)
        f = {k: v for k, v in kwargs.items()}
        f = {}
        Id = mongo_stuff.insert(self.db_files, f)
        return self.get_file(Id)

    @check.reqs(['callback'])
    def register_machine(self, **kwargs):
        m = {k: v for k, v in kwargs.items()}
        r = mongo_stuff.insert_or_override(self.db_machines, m)
        print('registered', r)
        return r

    def unreg_file(self, Id):
        return bool(
            self.db_files.delete_one({
                '_id': ObjectId(Id)
            }).deleted_count)

    @check.reqs(['machine_id'])
    def unreg_machine(self, machine_id):
        self.db_files.delete_many({'machine_id': machine_id})
        return bool(
            self.db_machines.delete_many({
                '_id': ObjectId(machine_id)
            }).deleted_count)

    # retreive files
    def get_file(self, Id):
        f = self.db_files.find_one({'_id': ObjectId(Id)})
        if f:
            return f
        else:
            raise my_errors.not_found

    def get_machine(self, Id):
        m = self.db_machines.find_one({'_id': ObjectId(Id)})
        if m:
            return m
        else:
            raise my_errors.not_found

    def search_filename(self, name):
        # search via name, returns list
        files = self.db_files.find({'name': name})
        if files:
            return [f for f in files]
        else:
            print("file name not found")
            raise my_errors.not_found
