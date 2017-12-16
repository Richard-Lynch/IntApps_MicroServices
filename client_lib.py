#!/Users/richie/miniconda3/bin/python3

from collections import defaultdict
import requests
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)
import send_securily
import decrypt_message
import check
import catch
from pprint import pprint


def print_response(f):
    def wrapped_f(*args, **kwargs):
        r = f(*args, **kwargs)

        if r is None:
            print('no response')
            return {'message': {}, 'code': 0}
        print('response:', r['code'])
        print('json:')
        pprint(r['message'])
        return r

    return wrapped_f


class DFS_client():
    def __init__(self, username, password):
        print('creating user')
        self.username = username
        self.password = password
        self.key = password
        self.token = password.encode()
        self.public_key = 'this simulates a public private key pair'
        print('u', self.username)
        print('p', self.password)
        print('k', self.key)
        self.get_addresses()
        print('user created')

    # interal funcs
    def get_addresses(self):
        # this should call registry server
        print('getting addresses')
        self.auth_address = 'http://127.0.0.1:8083/auth'
        self.files_address = 'http://127.0.0.1:8080/files'
        self.file_address = 'http://127.0.0.1:8080/file'
        self.dir_address = 'http://127.0.0.1:8081/dirs'
        self.lock_address = 'http://127.0.0.1:8084/lock'

    def extract_token(f):
        def wrapped_f(self, *args, **kwargs):
            r = f(self, *args, **kwargs)
            try:
                self.token = r.json()['token'].encode()
                self.key = r.json()['key']
                return r
            except Exception:
                print('token not in json')
                return r

        return wrapped_f

    @print_response
    @catch.dead
    @decrypt_message.with_key
    @send_securily.with_credentials
    def create_user(self, *args, **kwargs):
        print('createing user')
        pprint(kwargs)
        r = requests.post(self.auth_address, **kwargs)
        return r

    # auth utils
    @print_response
    @catch.dead
    @decrypt_message.with_key
    @send_securily.with_credentials
    def check_auth(self, *args, **kwargs):
        print('checking auth')
        r = requests.get(self.auth_address, **kwargs)
        return r

    @print_response
    @catch.dead
    @extract_token
    @decrypt_message.with_key
    @send_securily.with_credentials
    def generate_token(self, *args, **kwargs):
        print('generating token')
        r = requests.put(self.auth_address, **kwargs)
        return r

    @print_response
    @catch.dead
    @decrypt_message.with_key
    @send_securily.with_key
    def search_for_file(self, *args, **kwargs):
        print('searching for file')
        return requests.get(self.dir_address + '/search', **kwargs)

    @print_response
    @catch.dead
    @decrypt_message.with_key
    @send_securily.with_key
    def get_all_files(self, *args, **kwargs):
        print('getting all files')
        return requests.get(self.files_address, **kwargs)

    @print_response
    @catch.dead
    @decrypt_message.with_key
    @send_securily.with_key
    def get_file(self, *args, **kwargs):
        print('getting file')
        return requests.get(self.file_address, **kwargs)

    @print_response
    @catch.dead
    @decrypt_message.with_key
    @send_securily.with_key
    def add_file(self, *args, **kwargs):
        print('add file')
        return requests.post(self.files_address, **kwargs)

    @print_response
    @catch.dead
    @decrypt_message.with_key
    @send_securily.with_key
    def edit_file(self, *args, **kwargs):
        print('edit file')
        return requests.put(self.file_address, **kwargs)

    @print_response
    @catch.dead
    @decrypt_message.with_key
    @send_securily.with_key
    def del_file(self, *args, **kwargs):
        print('deleting')
        return requests.delete(self.file_address, **kwargs)

    @print_response
    @catch.dead
    @decrypt_message.with_key
    @send_securily.with_key
    def lock_file(self, *args, **kwargs):
        print('lock')
        return requests.post(self.lock_address, **kwargs)

    @print_response
    @catch.dead
    @decrypt_message.with_key
    @send_securily.with_key
    def unlock_file(self, *args, **kwargs):
        print('unlock')
        return requests.delete(self.lock_address, **kwargs)

    @print_response
    @catch.dead
    @decrypt_message.with_key
    @send_securily.with_key
    def check_lock_file(self, *args, **kwargs):
        print('check lock')
        return requests.get(self.lock_address, **kwargs)
