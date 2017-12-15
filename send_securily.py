#!/usr/local/bin/python3

import check
import my_errors
my_errors.make_classes(my_errors.errors)
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)


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


def with_token(f):
    def encrypt_message(message, key):
        s = Serializer(key)
        return s.dumps(message).decode()

    def wrapped_f(self, *args, **kwargs):
        key, r = f(self, *args, **kwargs)
        return encrypt_message(r, key)

    return wrapped_f
