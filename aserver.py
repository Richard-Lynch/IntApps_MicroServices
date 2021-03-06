#!/usr/local/bin/python3
# geneal
import secrets
import string
from pprint import pprint
# my utils
import my_errors
my_errors.make_classes(my_errors.errors)
import my_fields
import check
# --- mongo ----
from pymongo import MongoClient
import mongo_stuff
# --- security --
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import decrypt_message
import send_securily
import auth_with


class authServer():
    """
    Server providing authorization for clients/servers via 3 key mutual
    """

    def __init__(self,
                 secret_key='the quick brown fox jumps over the lazy dog',
                 public_key='this simulates a public private key pair',
                 expiration=600):
        self.load_users()
        self.s = Serializer(secret_key, expires_in=expiration)
        self.s_pub = Serializer(public_key, expires_in=expiration)

    def key_generator(self,
                      size=24,
                      chars=(string.ascii_letters + string.digits)):
        """Generate a psuedo random string of ascii letters and numbers"""
        return ''.join(
            secrets.SystemRandom().choice(chars) for _ in range(size))

    def load_users(self):
        """Load persistent storage of registered users"""
        self.db_users = MongoClient().test_database.db.users
        # drop db for testing, will not be in deployed version
        self.db_users.drop()
        # print(self.db_users)
        # create default admin user... clearly this should be much more secure!
        mongo_stuff.insert(
            self.db_users, {
                'username': 'admin',
                'password': 'admin',
                'password_hash': pwd_context.encrypt('admin'),
                'admin': True,
            })
        return True

    @send_securily.with_their_password
    @decrypt_message.with_public_key
    @auth_with.credentials
    @check.reqs(['username', 'password', 'admin'])
    def create_user(self, admin_data, **kwargs):
        """Create a new user. Requires admin privelages"""
        username = kwargs.get('username')
        password = kwargs.get('password')
        password_hash = pwd_context.encrypt(password)
        admin = kwargs.get('admin')
        if username is None or password is None or admin is None:
            raise my_errors.unauthorized_bad_request
        # NOTE: password should not be stored here,
        # and is not used anywhere else in the code,
        # it is only stored for testing purposes
        r = mongo_stuff.insert(
            self.db_users, {
                'username': username,
                'password': password,
                'password_hash': password_hash,
                'admin': admin
            })
        return {'created': bool(r)}

    @send_securily.with_their_password
    @decrypt_message.with_public_key
    @auth_with.credentials
    def generate_token(self, user_data, **kwargs):
        """Generate a unique token with a timeout"""
        user_data['_id'] = str(user_data['_id'])
        key = self.key_generator()
        user_data['key'] = key
        d = self.s.dumps(user_data).decode()
        return {'token': d, 'key': key}

    @send_securily.with_their_password
    @decrypt_message.with_public_key
    @auth_with.credentials
    def get_auth_level(self, user_data, **kwargs):
        """Return the authorization level of the user"""
        admin = user_data.get('admin')
        return {'auth': True, 'admin': admin}

    def verify_user(self, username, password):
        """Function which verifies a user is authorized"""
        # print('verifying')
        user_data = self.db_users.find_one({'username': username})
        if user_data:
            if pwd_context.verify(password, user_data['password_hash']):
                return user_data
            else:
                # NOTE: insecure, shouldnot specifcy wrong password
                raise my_errors.unauthorized_bad_password
        else:
            raise my_errors.unauthorized_user_not_found
