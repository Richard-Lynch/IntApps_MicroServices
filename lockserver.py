#!/usr/local/bin/python3
import my_errors
my_errors.make_classes(my_errors.errors)
import my_fields
import check
# --- mongo ----
from pymongo import MongoClient
from bson.objectid import ObjectId
import mongo_stuff


class lockServer():
    def __init__(self):
        self.load_locks()

    def load_locks(self):
        self.db_locks = MongoClient().test_database.db.locks
        # drop db for testing, will not be in deployed version
        self.db_locks.drop()
        print(self.db_locks)
        return True

    @check.reqs(['uri'])  # now takes args from parser as arg
    def lock_file(self, **kwargs):
        return bool(mongo_stuff.insert(self.db_locks, kwargs))

    @check.reqs(['uri'])  # now takes args from parser as arg
    def get_lock_status(self, **kwargs):
        return bool(self.db_locks.find_one(kwargs))

    @check.reqs(['uri'])  # now takes args from parser as arg
    def unlock_file(self, **kwargs):
        bool(self.db_locks.delete_one(kwargs).deleted_count)
