#!/usr/local/bin/python3
# general
from pprint import pprint
# my utisl
import my_errors
my_errors.make_classes(my_errors.errors)
import my_fields
import check
# --- Security ----
import decrypt_message
import send_securily
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# --- mongo ----
from pymongo import MongoClient
from bson.objectid import ObjectId
import mongo_stuff


class lockServer():
    """
    Server Providing a locking service to clients
    """

    def __init__(self,
                 secret_key='the quick brown fox jumps over the lazy dog'):
        self.s = Serializer(secret_key)
        self.load_locks()

    def load_locks(self):
        """Load persistent storage of locks"""
        self.db_locks = MongoClient().test_database.db.locks
        # drop db for testing, will not be in deployed version
        self.db_locks.drop()
        # print(self.db_locks)
        return True

    @send_securily.with_token
    @decrypt_message.with_token
    @check.reqs(['uri', '_fid'])
    def lock_file(self, **kwargs):
        """Attempt to lock a file by uri and file id(_fid)"""
        # print('in lock file')
        # locks = self.db_locks.find()
        # pprint([l for l in locks])
        return {'locked': bool(mongo_stuff.insert(self.db_locks, kwargs))}

    @send_securily.with_token
    @decrypt_message.with_token
    @check.reqs(['uri', '_fid'])
    def get_lock_status(self, **kwargs):
        """Get lock status of file by uri and file id(_fid)"""
        # print('in get lock status')
        return {'is_locked': bool(self.db_locks.find_one(kwargs))}

    @send_securily.with_token
    @decrypt_message.with_token
    @check.reqs(['uri', '_fid'])  # now takes args from parser as arg
    def unlock_file(self, **kwargs):
        """Attemp to unlock a specific file by uri and file id(_fid)"""
        print('in unlock file')
        return {
            'unlocked': bool(self.db_locks.delete_one(kwargs).deleted_count)
        }
