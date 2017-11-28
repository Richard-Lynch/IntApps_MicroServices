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
        r = requests.post(self.dirServerAdd).json()
        self.machine_id = r.get('id', -1)
        self.register_initial_files()
        print ("file server started")

    def __open__(self):
        print("using fileServer as open")

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

# register
    def register_initial_files(self):
        for f in self.files:
            r = self.register_file(f)
            # should check here if r is correct/valid
            print (r)

    def register_file(self, f):
        # regsiter the file with the dir server
        return requests.put(self.dirServerAdd + '/regsiter', \
                json=dict( marshal( f, my_fields.register_fields ) ) \
                ).json()

    def un_register_file(self, id):
        # unregister with the dir server 
        f = self.get_file(id)
        # return the response from the request
        return requests.delete(f['reg_uri']).json()

    def un_register_all_files(self):
        print ("in all")
        return requests.delete(self.dirServerAdd + '/regsiter', \
                json={'machine_id' : self.machine_id}).json()
        for f in self.files:
            self.un_register_file(self.files[f]['Id'])
            # print ("id", self.files[f]['id'])
            # print ("result", self.un_register_file(self.files[f]['id']))

# file edits
    def add_file(self, **kwargs):
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
