#!/usr/local/bin/python3
import my_errors
my_errors.make_classes(my_errors.errors)
import my_fields
from collections import defaultdict
class dirServer():
    def __init__(self):
        self.next_machine = 0
        self.next_file_id = 0
        self.files = defaultdict(dict)
        self.files_id = defaultdict(dict)
        self.machines = defaultdict(dict)
    # util functions
    def get_next_machince(self):
        # lock
        next_machine = self.next_machine
        self.next_machine += 1 
        return next_machine

    def get_next_file_id(self):
        # lock
        current = self.next_file_id
        self.next_file_id += 1
        # release
        return current
    # registration
    def register_file(self, **kwargs):
        # create a blank file reg
        f = {}
        # for every keyword arg (filtered by api)
        for k, v in kwargs.items():
            # add an entry to the file reg
            f[k] = v
        # add dir server values
        id = self.get_next_file_id()
        f['id'] = id
        # map via id
        self.machines[f['id']] = f
        # map via name
        if f['name'] not in self.files:
            self.files[f['name']] = {f['id'] : f}
        else:
            self.files[f['name']][f['id']] = f
        # map via machine id
        if f['machine_id'] not in self.machines:
            self.machines[f['machine_id']] = {f['id'] : f}
        else:
            self.machines[f['machine_id']][f['id']] = f
        return f

    def unreg_file(self, id):
        file = self.get_file_by_id(id)
        del self.files_id[file['id']]
        del self.files[file['name']][id]
        del self.machines[file['machine_id']][id]

    # retreive files
    def get_file_by_id(self, id):
        # get via id
        try:
            return self.files_id[id]
        except KeyError:
            raise my_errors.not_found
    
    def search_filename(self, name):
        # search via name, returns list
        try:
            return [ v for v in self.files[name].values() ]
        except KeyError:
            raise my_errors.not_found

    def list_by_machine(self, machine_id):
        # search via machine_id, returns list
        try:
            return [ v for v in self.machines[machine_id].values() ]
        except KeyError:
            raise my_errors.not_found
        
