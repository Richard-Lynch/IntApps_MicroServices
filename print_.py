#!/usr/local/bin/python3
from pprint import pprint


def response(f):
    """Decorator to print the response from a server"""

    def wrapped_f(*args, **kwargs):
        r = f(*args, **kwargs)
        if type(r) is dict:
            print('response:', r['status'])
            print('json:')
            pprint(r['message'])
            print("DONE")
        elif r is None:
            print('no response')
            return {'message': {}, 'status': 0}
        else:
            print('response not dict')
            print('response', r)
        return r

    return wrapped_f
