#!/usr/local/bin/python3
import my_errors
my_errors.make_classes(my_errors.errors)
import my_fields
import check

class lockServer():
    def __init__(self):
        self.files = {}
        self.machines = {}

    @check.reqs(['uri']) # now takes args from parser as arg
    def lock_file(self, **kwargs):
        uri = kwargs.get('uri')
        if uri in self.files:
            return False
        else:
            self.files[uri] = True
            return True

    @check.reqs(['uri']) # now takes args from parser as arg
    def get_lock_status(self, **kwargs):
        uri = kwargs.get('uri')
        if uri in self.files:
            return True
        else:
            return False

    @check.reqs(['uri']) # now takes args from parser as arg
    def unlock_file(self, **kwargs):
        uri = kwargs.get('uri')
        if uri in self.files:
            del self.files[uri]
            return True
        else:
            return False
