#!/usr/local/bin/python3
import my_errors
my_errors.make_classes(my_errors.errors)
import my_fields
import check
# --- mongo ----
from pymongo import MongoClient
from bson.objectid import ObjectId
import mongo_stuff
# --- security --
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)


class authServer():
    def __init__(self,
                 secret_key='the quick brown fox jumps over the lazy dog',
                 expiration=600):
        self.load_users()
        self.s = Serializer(secret_key, expires_in=expiration)

    def load_users(self):
        self.db_users = MongoClient().test_database.db.users
        # drop db for testing, will not be in deployed version
        self.db_users.drop()
        print(self.db_users)
        # create default admin user... clearly this should be much more secure!
        mongo_stuff.insert(
            self.db_users, {
                'username': 'admin',
                'password': 'admin',
                'password_hash': pwd_context.encrypt('admin'),
                'admin': True,
            })
        return True

    # now takes args from parser as arg
    @check.reqs(['username', 'password', 'admin'])
    def create_user(self, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')
        password_hash = pwd_context.encrypt(password)
        admin = kwargs.get('admin')
        if username is None or password is None or admin is None:
            raise my_errors.bad_request
        # password should not be stored here, and is not used anywhere else in
        # the code, it is only stored for testing purposes
        return bool(
            mongo_stuff.insert(
                self.db_users, {
                    'username': username,
                    'password': password,
                    'password_hash': password_hash,
                    'admin': admin
                }))

    def verify_user(self, username, password):
        user_data = self.db_users.find_one({'username': username})
        if user_data:
            if pwd_context.verify(password, user_data['password_hash']):
                return user_data
            else:
                # return False
                raise my_errors.bad_password
        else:
            # return False
            raise my_errors.user_not_found
