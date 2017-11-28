#!/usr/local/bin/python3
import my_errors
my_errors.make_classes(my_errors.errors)
import my_fields
import check_reqs

# def check_reqs(reqs):
#     def wrap(f):
#         def wrapped_f(self, **args):
#             # ensure the requirements are met
#             if all (req in args for req in reqs):
#                 print ('reqs met')
#                 # filter un-required keywords
#                 kwargs = { req: args[req] for req in reqs }
#                 # call func
#                 return f(self, **kwargs)
#             else:
#                 raise my_errors.bad_request
#         return wrapped_f
#     return wrap

class lockServer():
    def __init__(self):
        self.files = {}
        self.machines = {}

    @check_reqs(['uri']) # now takes args from parser as arg
    def lock_file(self, **kwargs):
        uri = kwargs.get('uri')
        if uri in self.files:
            return False
        else:
            self.files[uri] = True
            return True

    @check_reqs(['uri']) # now takes args from parser as arg
    def get_lock_status(self, **kwargs):
        uri = kwargs.get('uri')
        if uri in self.files:
            return True
        else:
            return False

    @check_reqs(['uri']) # now takes args from parser as arg
    def unlock_file(self, **kwargs):
        uri = kwargs.get('uri')
        if uri in self.files:
            del self.files[uri]
            return True
        else:
            return False
