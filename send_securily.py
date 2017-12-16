#!/usr/local/bin/python3

import check
import my_errors
my_errors.make_classes(my_errors.errors)
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)
from pprint import pprint


def catch_decode(f):
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


@catch_decode
def with_key(f):
    def encrypt_message(message, key):
        s = Serializer(key)
        return s.dumps(message).decode()

    def wrapped_f(self, *args, **kwargs):
        message = encrypt_message({k: v for k, v in kwargs.items()}, self.key)
        kwargs = {}
        kwargs['json'] = {'token': self.token.decode(), 'message': message}
        return f(self, *args, **kwargs)

    return wrapped_f


@catch_decode
def with_token(f):
    def encrypt_message(message, key):
        s = Serializer(key)
        return s.dumps(message).decode()

    def wrapped_f(self, *args, **kwargs):
        key, r = f(self, *args, **kwargs)
        return encrypt_message(r, key)

    return wrapped_f


def with_credentials(f):
    def encrypt_message(message, key):
        s = Serializer(key)
        return s.dumps(message).decode()

    def wrapped_f(self, *args, **kwargs):
        print('in send with creds')
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
    def encrypt_message(message, key):
        s = Serializer(key)
        return s.dumps(message).decode()

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
    def encrypt_message(message, key):
        s = Serializer(key)
        return s.dumps(message).decode()

    def wrapped_f(self, *args, **kwargs):
        key, r = f(self, *args, **kwargs)
        return encrypt_message(r, key)

    return wrapped_f
