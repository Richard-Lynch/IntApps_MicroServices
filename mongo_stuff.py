#!/usr/local/bin/python3
import my_errors
my_errors.make_classes(my_errors.errors)

"""Provides some useful mongo db utils"""


def exists(collection, f):
    """Return true if a file exists"""
    return bool(collection.find(f, {'_id': 1}).limit(1).count())


def insert(collection, f):
    """Insert a file if its doesnt exist, and return its id"""
    if not exists(collection, f):
        fid = collection.insert_one(f).inserted_id
        return fid
    else:
        print('not inserting')
        raise my_errors.file_exists


def insert_or_override(collection, f):
    """Insert or override a file, and return the repsonse"""
    r = collection.find_one_and_update(
        f, {'$set': f}, upsert=True, return_new_document=True)
    return r
