#!/usr/local/bin/python3
import my_errors
my_errors.make_classes(my_errors.errors)
import my_fields
import check
# --- mongo ----
from pymongo import MongoClient
from bson.objectid import ObjectId
import mongo_stuff


class regServer():
    def __init__(self):
        self.load_regs()

    def load_regs(self):
        self.db_regs = MongoClient().test_database.db.regs
        # drop db for testing, will not be in deployed version
        self.db_regs.drop()
        print(self.db_regs)
        return True

    @check.reqs(['callback'])  # now takes args from parser as arg
    def reg_service(self, **kwargs):
        return bool(mongo_stuff.insert(self.db_regs, kwargs))

    @check.reqs(['type'])  # now takes args from parser as arg
    def get_reg_status(self, **kwargs):
        # TODO should do load balance
        return bool(self.db_regs.find_one(kwargs))

    @check.reqs(['callback'])  # now takes args from parser as arg
    def unreg_service(self, **kwargs):
        bool(self.db_regs.delete_one(kwargs).deleted_count)
