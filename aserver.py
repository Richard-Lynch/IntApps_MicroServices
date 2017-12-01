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
        return True

    @check.reqs(['username', 'password'])  # now takes args from parser as arg
    def create_user(self, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')
        password_hash = pwd_context.encrypt(password)
        if username is None or password is None:
            raise my_errors.bad_request
        return bool(
            mongo_stuff.insert(
                self.db_users, {
                    'username': username,
                    'password': password,
                    'password_hash': password_hash,
                }))

    def verify_user(self, username, password):
        try:
            user_data = self.db_users.find_one({'username': username})
            if pwd_context.verify(password, user_data['password_hash']):
                return user_data
            else:
                return False
                raise my_errors.unauthorized
        except Exception:
            return False
            raise my_errors.unauthorized
