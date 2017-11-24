#!/usr/local/bin/python3
class dirServer():
    def __init__(self):
        self.next_machine = 0
        self.files = {}
        self.machines = {}
    def get_next_machince(self):
        # lock
        next_machine = self.next_machine
        self.next_machine += 1 
        return next_machine
    def register_file(self, args):
        name = args['name']
        machine_id = args['machine_id']
        f = {}
        for k, v in args.items():
            f[k] = v
        if name not in self.files:
            # f['id'] = files[-1]['id'] + 1
            self.files[name] = [f]
        else:
            self.files[name].append(f)
        if machine_id not in self.machines:
            self.machines[machine_id] = [f]
        else:
            self.machines[machine_id].append(f)
        return f
    def get_file(self, args):
        f = [ self.files[f] for f in self.files if self.files[f]['name'] == name ]
        if len(f) > 0:
            return f[0]
        else:
            return None
    def del_file(self, name):
        f = self.get_file(name)
        if f != None:
            self.files.remove(f)
            return f
        else:
            return None
