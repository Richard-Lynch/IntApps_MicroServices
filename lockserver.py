#!/usr/local/bin/python3
class lockServer():
    def __init__(self):
        self.files = {}
        self.machines = {}
    def lock_file(self, uri):
        if uri in self.files:
            return False
        else:
            self.files[uri] = True
            return True
    def get_lock_status(self, uri):
        if uri in self.files:
            return True
        else:
            return False
    def unlock_file(self, uri):
        if uri in self.files:
            del self.files[uri]
            return True
        else:
            return False
