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
        self.files_Id = {}
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
        # reg file, add every keyword arg (filtered by api)
        f = {k: v for k, v in kwargs.items()}
        # add dir server values
        Id = self.get_next_file_id()
        f['Id'] = Id
        # map via id
        self.files_Id[f['Id']] = f
        # map via name
        self.files[f['name']][f['Id']] = f
        # map via machine id
        self.machines[f['machine_id']][f['Id']] = f
        return f

    def unreg_file(self, Id):
        file = self.get_file_by_Id(Id)
        del self.files_Id[Id]
        del self.files[file['name']][Id]
        del self.machines[file['machine_id']][Id]
        return file

    def unreg_machine(self, machine_id):
        # get all files from machine_id
        try:
            machine = self.machines[machine_id]
        except KeyError:
            raise my_errors.not_found
        Ids = [ Id for Id in machine.keys() ]
        for Id in Ids:
            self.unreg_file(Id)
        del self.machines[machine_id]
        return machine_id



    # retreive files
    def get_file_by_Id(self, Id):
        # get via Id
        try:
            return self.files_Id[Id]
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
        
