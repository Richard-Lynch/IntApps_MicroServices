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

class fileServer():
    def __init__(self):
        self.file_names = {}
        self.files = {}
        self.load_files()
        self.next_id = 0
        self.dirServerAdd = "http://127.0.0.1:8081/dirs"
        r = requests.post(self.dirServerAdd+'/register').json()
        self.machine_id = r.get('Id', -1)
        self.register_initial_files()
        print ("file server started")

    def __enter__(self):
        print("using fileServer as open")
        return self

    def __del__(self):
        print("deleting")
        self.un_register_all_files()

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

    def register_file(self, f):
        # regsiter the file with the dir server
        r = requests.put(self.dirServerAdd + '/register', \
                json=dict( marshal( f, my_fields.register_fields ) )).json()
        print (r)
        return r

    def un_register_file(self, id):
        # unregister with the dir server 
        f = self.get_file(id)
        # return the response from the request
        return requests.delete(f['reg_uri']).json()

    def un_register_all_files(self):
        # for when a machine is going down
        print ("in all")
        r = requests.delete(self.dirServerAdd + '/register', \
                json={'machine_id' : self.machine_id}).json()
        print (r)

# file edits
    def add_file(self, **kwargs):
        print ('in add_file')
        # add every keyword arg (filtered by api)
        f = { k: v for k, v in kwargs.items()}
        # if the filename already exist
        if f['name'] in self.file_names:
            raise my_errors.file_exists
        # set file server values
        Id = self.get_next_id()
        f['Id'] = Id
        f['machine_id'] = self.machine_id
        f['reg_uri'] = self.register_file(f)['file']['reg_uri']
        # map via id
        self.files[Id]= f
        # map via name
        self.file_names[f['name']] = f
        return f

    def update_file(self, args, Id):
        # update a file on the fileserver
        f = self.get_file(Id)
        for k, v in args.items():
            if v != None:
                f[k] = v
        return f

    def del_file(self, Id):
        # delete a file from the server
        f = self.get_file(Id)
        self.un_register(Id)
        del self.files[Id]
        del self.files[f['name']]
        return True

# return files
    def get_file(self, Id):
        try:
            return self.files[Id]
        except KeyError:
            raise my_errors.not_found

    def get_all_files(self):
        # return a list of values
        return [ v for v in self.files.values() ]
