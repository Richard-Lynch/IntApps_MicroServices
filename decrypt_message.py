#!/usr/local/bin/python3
import check
import my_errors
my_errors.make_classes(my_errors.errors)
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer)
import catch
"""
Provides a number of decorators to decode encrypted messages.

Each of these decorators will decrypt a corresponding encryption 
from its pair module 'send_securily' 
"""


def decrypt_m(message, key):
    s = Serializer(key)
    return s.loads(message)


@catch.decode
def with_token(f):
    @check.reqs(['token', 'message'])
    def wrapped_f(self, *args, **kwargs):
        token = kwargs.get('token')
        message = kwargs.get('message')
        data = self.s.loads(token)
        s = Serializer(data['key'])
        decoded_message = s.loads(message)
        return data['key'], f(self, *args, **decoded_message)

    return wrapped_f


@catch.decode
def with_key(f):
    def wrapped_f(self, *args, **kwargs):
        r = f(self, *args, **kwargs)
        if r.status_code != 200:
            return {'status': r.status_code, 'message': r.json()}

        message = r.json()['message']
        c = r.status_code
        decoded_message = decrypt_m(message, self.key)
        return {'status': c, 'message': decoded_message}

    return wrapped_f


@catch.decode
def with_password(f):
    def wrapped_f(self, *args, **kwargs):
        r = f(self, *args, **kwargs)
        if r.status_code != 200:
            return {'status': r.status_code, 'message': r.json()}

        message = r.json()['message']
        c = r.status_code
        decoded_message = decrypt_m(message, self.password)
        return {'status': c, 'message': decoded_message}

    return wrapped_f


@catch.decode
def with_public_key(f):
    @check.reqs(['message'])
    def wrapped_f(self, *args, **kwargs):
        message = kwargs.get('message')
        decoded_message = self.s_pub.loads(message)
        return f(self, *args, **decoded_message)

    return wrapped_f
