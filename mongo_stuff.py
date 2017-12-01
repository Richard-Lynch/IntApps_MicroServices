#!/usr/local/bin/python3

# from pymongo import MongoClient
# from pprint import pprint
# from bson.objectid import ObjectId
# import sys
import my_errors
my_errors.make_classes(my_errors.errors)


def exists(collection, f):
    return bool(collection.find(f, {'_id': 1}).limit(1).count())


def insert(collection, f):
    if not exists(collection, f):
        print('inserting')
        fid = collection.insert_one(f).inserted_id
        print("fid", fid)
        return fid
    else:
        print('not inserting')
        raise my_errors.file_exists


def insert_or_override(collection, f):
    r = collection.find_one_and_update(
        f, {'$set': f}, upsert=True, return_new_document=True)
    return r
