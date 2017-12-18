#!/usr/local/bin/python3


def check(f):
    """A decorator checking for a file in cache before making request"""

    def wrapped_f(self, *args, **kwargs):
        if kwargs['_id'] in self.cached_files:
            cached_file = self.get_from_cache(kwargs['_id'])
            return {'status': 200, 'message': {'file': cached_file}}
        else:
            r = f(self, *args, **kwargs)
            if r['status'] == 200:
                self.add_to_cache(r['message']['file'])
            return r

    return wrapped_f


def update_on_add(f):
    """A decorator updating cache when a new file is addded"""

    def wrapped_f(self, *args, **kwargs):
        r = f(self, *args, **kwargs)
        if r['status'] == 200:
            self.add_to_cache({**kwargs, **r['message']['file']})
        return r

    return wrapped_f


def update_on_edit(f):
    """A decorator updating cache when a file is edited"""

    def wrapped_f(self, *args, **kwargs):
        r = f(self, *args, **kwargs)
        if r['status'] == 200:
            self.add_to_cache({**kwargs, **r['message']['file']})
        else:
            # there should be some code here to deal with
            # the file not being allowed to update,
            # as it may be a version issue!
            print('file not updated succesfuly!')
        return r

    return wrapped_f
