#!/usr/local/bin/python3
import my_errors
my_errors.make_classes(my_errors.errors)
import my_fields
import check
import decrypt_message
import send_securily
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from pprint import pprint
# --- mongo ----
from pymongo import MongoClient
from bson.objectid import ObjectId
import mongo_stuff


class lockServer():
    def __init__(self,
                 secret_key='the quick brown fox jumps over the lazy dog'):
        self.s = Serializer(secret_key)
        self.load_locks()

    def load_locks(self):
        self.db_locks = MongoClient().test_database.db.locks
        # drop db for testing, will not be in deployed version
        self.db_locks.drop()
        print(self.db_locks)
        return True

    @send_securily.with_token
    @decrypt_message.with_token
    @check.reqs(['uri', '_fid'])  # now takes args from parser as arg
    def lock_file(self, **kwargs):
        locks = self.db_locks.find()
        pprint([l for l in locks])
        r = {'locked': bool(mongo_stuff.insert(self.db_locks, kwargs))}
        print(r)
        return r

    @send_securily.with_token
    @decrypt_message.with_token
    @check.reqs(['uri', '_fid'])  # now takes args from parser as arg
    def get_lock_status(self, **kwargs):
        r = {'is_locked': bool(self.db_locks.find_one(kwargs))}
        print(r)
        return r

    @send_securily.with_token
    @decrypt_message.with_token
    @check.reqs(['uri', '_fid'])  # now takes args from parser as arg
    def unlock_file(self, **kwargs):
        r = {'unlocked': bool(self.db_locks.delete_one(kwargs).deleted_count)}
        print(r)
        return r
