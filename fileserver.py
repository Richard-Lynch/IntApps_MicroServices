#!/usr/local/bin/python3
import requests
import sys
from flask import Flask, jsonify, request, make_response, url_for
from flask_kerberos import requires_authentication
from flask_restful import Api, Resource, abort, HTTPException
from flask_restful import reqparse, fields, marshal
from my_fields import *
class fileServer():
    def __init__(self):
        self.files = self.load_files()
        self.next_id = 1
        self.dirServerAdd = "http://127.0.0.1:8081/files"
        r = requests.post(self.dirServerAdd).json()
        self.machine_id = None
        if 'id' in r:
            self.machine_id = r['id']
            self.register_initial_files()
            print ("file server started")
        else:
            print ("not given id")
# util functions
    def load_files(self):
        return {}
    def get_next(self):
        # lock
        current = self.next_id
        self.next_id += 1
        # release
        return current
# register
    def register_initial_files(self):
        if len (self.files) > 0:
            for f in self.files:
                r = self.register_file(f)
                print (r)
    def register_file(self, f):
        return requests.put(self.dirServerAdd, json=dict(marshal(f, register_fields))).json
    def un_register_file(self, id):
        f = get_file(id)
        return requests.delete(f['url']).json
# file edits
    def add_file(self, args):
        f = {}
        # do any checking here
        if 'name' in args.keys():
            if args.get('name') in self.files:
                return None
        for k, v in args.items():
            f[k] = v
        f['id'] = self.get_next()
        f['machine_id'] = self.machine_id
        r = self.register_file(f)
        self.files[f['name']] = f
        return f
    def update_file(self, args, id):
        f = self.get_file(id)
        if f != None:
            for k, v in args.items():
                if v != None:
                    f[k] = v
        return f
    def del_file(self, id):
        f = self.get_file(id)
        if f == None:
            return False
        self.un_register(id)
        self.files.remove(file)
        return True
# return files
    def get_file(self, id):
        f = [ self.files[f] for f in self.files if self.files[f]['id'] == id ]
        print ('f', f)
        # f = list(filter(lambda F: self.files[F]['id'] == id, self.files))
        if len(f) > 0:
            return f[0]
        else:
            return None
    def get_all_files(self):
        return self.files
