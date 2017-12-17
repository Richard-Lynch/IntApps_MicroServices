#!/usr/local/bin/python3


def check(f):
    def wrapped_f(self, *args, **kwargs):
        # print('in cache')
        if kwargs['_id'] in self.cached_files:
            # print('file is cached')
            cached_file = self.get_from_cache(kwargs['_id'])
            return {'status': 200, 'message': {'file': cached_file}}
        else:
            # print('file is not cached')
            r = f(self, *args, **kwargs)
            if r['status'] == 200:
                self.add_to_cache(r['message']['file'])
            return r

    return wrapped_f


def update_on_add(f):
    def wrapped_f(self, *args, **kwargs):
        # print('in update cache on add')
        r = f(self, *args, **kwargs)
        if r['status'] == 200:
            self.add_to_cache({**kwargs, **r['message']['file']})
        return r

    return wrapped_f


def update_on_edit(f):
    def wrapped_f(self, *args, **kwargs):
        # print('in update cache on edit')
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
