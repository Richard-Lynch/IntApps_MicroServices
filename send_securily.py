#!/usr/local/bin/python3
import my_errors
my_errors.make_classes(my_errors.errors)
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer)
import catch
"""
Provides a number of decorators to encrypt messages.

Each of these decorators will need to be decrypted with 
a corresponding decrypter from its pair module 'decrypt_message' 
"""


def encrypt_message(message, key):
    s = Serializer(key)
    return s.dumps(message).decode()


@catch.decode
def with_key(f):
    def wrapped_f(self, *args, **kwargs):
        message = encrypt_message({k: v for k, v in kwargs.items()}, self.key)
        kwargs = {}
        kwargs['json'] = {'token': self.token.decode(), 'message': message}
        return f(self, *args, **kwargs)

    return wrapped_f


@catch.decode
def with_token(f):
    def wrapped_f(self, *args, **kwargs):
        key, r = f(self, *args, **kwargs)
        return encrypt_message(r, key)

    return wrapped_f


def with_credentials(f):
    def wrapped_f(self, *args, **kwargs):
        message = {k: v for k, v in kwargs.items()}
        auth = {'username': self.username, 'password': self.password}
        message = {'message': message, 'auth': auth}
        message = encrypt_message(message, self.public_key)
        payload = {}
        payload['json'] = {'message': message}
        r = f(self, *args, **payload)
        return r

    return wrapped_f


def with_admin_password(f):
    def wrapped_f(self, credentials, *args, **kwargs):
        message = encrypt_message({k: v
                                   for k, v in kwargs.items()},
                                  self.public_key)
        payload = {}
        payload['json'] = {'message': message}
        payload['auth'] = credentials
        r = f(self, *args, **payload)
        return r

    return wrapped_f


def with_their_password(f):
    def wrapped_f(self, *args, **kwargs):
        key, r = f(self, *args, **kwargs)
        return encrypt_message(r, key)

    return wrapped_f
