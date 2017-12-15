#!/usr/local/bin/python3
import check
import my_errors
my_errors.make_classes(my_errors.errors)
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)


def with_token(f):
    @check.reqs(['token', 'message'])
    def wrapped_f(self, *args, **kwargs):
        token = kwargs.get('token')
        message = kwargs.get('message')
        try:
            # TODO not using anything except key and timeout for now, but
            # could have other info in the token like permissions etc
            data = self.s.loads(token)
            s = Serializer(data['key'])
            decoded_message = s.loads(message)
            return data['key'], f(self, *args, **decoded_message)
        except SignatureExpired:
            print('exp')
            # TODO change to sigexpired
            raise my_errors.unauthorized
        except BadSignature:
            print('bad')
            # TODO change to badsig
            raise my_errors.unauthorized
        except Exception as e:
            # TODO change to unknown exception
            # TODO catching get_file raise
            # print('e', e)
            raise my_errors.bad_request

    return wrapped_f


def with_key(f):
    def decrypt_m(message, key):
        try:
            s = Serializer(key)
            return s.loads(message)
        except SignatureExpired:
            print('exp')
            # TODO change to sigexpired
            raise my_errors.unauthorized
        except BadSignature:
            print('bad')
            # TODO change to badsig
            raise my_errors.unauthorized
        except Exception as e:
            print('error', e)

    def wrapped_f(self, *args, **kwargs):
        try:
            r = f(self, *args, **kwargs)
            message = r.json()['message']
            c = r.status_code
            # TODO not using anything except key and timeout for now, but
            # could have other info in the token like permissions etc
            decoded_message = decrypt_m(message, self.key)
            return {'code': c, 'message': decoded_message}
        except Exception as e:
            # TODO change to unknown exception
            # TODO catching get_file raise
            # print('e', e)
            raise my_errors.bad_request

    return wrapped_f
