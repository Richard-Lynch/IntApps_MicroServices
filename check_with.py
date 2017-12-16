#!/usr/local/bin/python3

import secrets
import string
import my_errors
my_errors.make_classes(my_errors.errors)
import my_fields
import check
import decrypt_message
import send_securily
from pprint import pprint
# --- mongo ----
from pymongo import MongoClient
import mongo_stuff
# --- security --
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


def credentials(f):
    @check.reqs(['auth', 'message'])
    def wrapped_f(self, *args, **kwargs):
        print('in checked')
        auth = kwargs.get('auth')
        message = kwargs.get('message')
        try:
            user_data = self.verify_user(**auth)
            return auth['password'], f(self, user_data, *args, **message)
        except Exception as e:
            print('exception in check with c')
            print(e)
            raise

    return wrapped_f
