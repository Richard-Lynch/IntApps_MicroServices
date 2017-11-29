#!/usr/local/bin/python3
import requests
import sys
from flask import Flask, jsonify, request, make_response, url_for
from flask_kerberos import requires_authentication
from flask_restful import Api, Resource, abort, HTTPException
from flask_restful import reqparse, fields, marshal
from collections import defaultdict
import my_errors
my_errors.make_classes(my_errors.errors)
import my_fields
import check
# --- mongo ----
from pymongo import MongoClient
from pprint import pprint 
from bson.objectid import ObjectId
import mongo_stuff

class fileServer():
    def __init__(self):
        # mongo
        client = MongoClient()
        self.db = client.test_database
        print(self.db)
        self.collection = self.db.test_collection
        print (self.collection)
        self.db_files = self.db.files
        self.db_files.drop()
        print (self.db_files)
        # main
        self.file_names = {}
        self.files = {}
        self.load_files()
        self.next_id = 0
        self.dirServerAdd = "http://127.0.0.1:8081/dirs"
        r = requests.post(self.dirServerAdd+'/register').json()
        self.machine_id = r.get('_id', -1)
        self.register_initial_files()
        print ("file server started")

    def __enter__(self):
        print("using fileServer as open")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("exiting")
        self.un_register_all_files()

# util functions
    def load_files(self):
        return True

    def get_next_id(self):
        # lock
        current = self.next_id
        self.next_id += 1
        # release
        return current

    def del_all_files(self):
        # for testing only, would not be live
        self.file_names = {}
        self.files = {}
        self.un_register_all_files()

# register
    def register_initial_files(self):
        for f in self.files:
            r = self.register_file(f)
            # should check here if r is correct/valid
            print (r)

    def register_file(self, Id):
        # regsiter the file with the dir server
        f = self.db_files.find_one({'_id' : Id})
        if f:
            r = requests.put(self.dirServerAdd + '/register', \
                    json=dict( marshal( f, my_fields.register_fields ) )).json()
            print ('r',r)
            try:
                reg_uri = r['file']['reg_uri']
                self.db_files.update_one({'_id':ObjectId(Id)}, \
                        {'$set':{'reg_uri':reg_uri}})
            except Exception:
                raise my_errors.bad_request
        else:
            raise my_errors.bad_request

    def un_register_file(self, Id):
        # unregister with the dir server 
        f = self.get_file(Id)
        # return the response from the request
        return requests.delete(f['reg_uri']).json()

    def un_register_all_files(self):
        # for when a machine is going down
        print ("in all")
        r = requests.delete(self.dirServerAdd + '/register', \
                json={'machine_id' : self.machine_id}).json()
        print (r)

# file edits
    @check.reqs(['name', 'content'])
    def add_file(self, **kwargs):
        # add every keyword arg (filtered by api)
        f = { k: v for k, v in kwargs.items()}
        f['machine_id'] = self.machine_id
        Id = mongo_stuff.insert(self.db_files, f)
        self.register_file(Id)
        return self.get_file(Id)

    def update_file(self, args, Id):
        # filter the args, if none dont set
        kwargs = {k : v for k, v in args.items() if v}
        # update a file on the fileserver
        self.db_files.update_one({'_id' : ObjectId(Id)}, {'$set': kwargs })
        return self.get_file(Id)

    def del_file(self, Id):
        # delete a file from the server
        self.un_register(Id)
        return bool(self.db_files.delete_one({'_id' : ObjectId(Id)}).deleted_count)

# return files
    def get_file(self, Id):
        f = self.db_files.find_one({'_id' : ObjectId(Id)})
        if f:
            return f
        else:
            raise my_errors.not_found

    def get_all_files(self):
        # return a list of values
        return [ f for f in self.db_files.find() ]
