#!/usr/local/bin/python3

import my_errors
my_errors.make_classes(my_errors.errors)
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)
import requests


def decode(f):
    def wrapped_f(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except SignatureExpired:
            print('exp')
            raise my_errors.unauthorized_sig_expired
        except BadSignature:
            print('bad')
            raise my_errors.unauthorized_bad_sig
        except Exception:
            raise

    return wrapped_f


def dead(f):
    def wrapped_f(*args, **kwargs):
        try:
            r = f(*args, **kwargs)
            return r
        except requests.exceptions.ConnectionError as e:
            # at this point, the request has been rejected
            # by which ever server was being contacted.
            # it would be a good option for this handler
            # to call 'self.refresh_machines()', which should call
            # to the registry server to get one or more new server
            # addresses to use
            print('connection error')
            print(e)
        except Exception as e:
            print('exception in catch')
            print('e', e)
        return {'message': {}, 'code': 0}

    return wrapped_f
