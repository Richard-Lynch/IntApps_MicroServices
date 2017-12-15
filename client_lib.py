#!/Users/richie/miniconda3/bin/python3

from collections import defaultdict
import requests
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)
import send_securily
import decrypt_message
import check
from pprint import pprint


def print_requests_response(f):
    def wrapped_f(*args, **kwargs):
        r = f(*args, **kwargs)
        print('response:', r)
        print('json', r.json())
        return r

    return wrapped_f


def print_response(f):
    def wrapped_f(*args, **kwargs):
        r = f(*args, **kwargs)
        if r is None:
            print('no response')
            return None
        print('response:', r['code'])
        print('json:')
        pprint(r['message'])
        return r

    return wrapped_f


class DFS_client():
    def __init__(self, username, password):
        print('creating user')
        auth_address = 'http://127.0.0.1:8083/auth'
        demo_address = 'http://127.0.0.1:8085/token'
        file_address = 'http://127.0.0.1:8080/files'
        self.addresses = {
            'file_server': file_address,
            'auth_server': auth_address,
            'demo_server': demo_address,
        }

        self.auth_address = 'http://127.0.0.1:8083/auth'
        self.files_address = 'http://127.0.0.1:8080/files'
        self.file_address = 'http://127.0.0.1:8080/file'
        self.dir_address = 'http://127.0.0.1:8081/dirs'
        # self.dir_address = 'http://127.0.0.1:8081/dirs/search'
        # self.dir_address = 'http://127.0.0.1:8081/dirs/files'
        self.username = username
        self.password = password
        print('u', self.username)
        print('p', self.password)

    # admin tools
    @print_requests_response
    def create_user(self,
                    admin_username='admin',
                    admin_password='admin',
                    username=None,
                    password=None,
                    admin=False):
        print('createing user')
        if username is None:
            username = self.username
        r = requests.post(
            self.auth_address,
            json={'username': username,
                  'password': password,
                  'admin': admin},
            auth=(admin_username, admin_password))
        return r

    # auth utils
    @print_requests_response
    def check_auth(self, username=None, password=None):
        print('checking auth')
        if username is None:
            username = self.username
        if password is None:
            password = self.password
        r = requests.get(self.auth_address, auth=(username, password))
        return r

    @print_requests_response
    def generate_token(self):
        print('generating token')
        r = requests.put(
            self.auth_address, auth=(self.username, self.password))
        try:
            self.token = r.json()['token'].encode()
            self.key = r.json()['key']
            return r
        except Exception:
            print('token not in json')
            return r

    @print_response
    @decrypt_message.with_key
    @send_securily.with_key
    def search_for_file(self, *args, **kwargs):
        print('searchign for file')
        return requests.get(self.dir_address + '/search', **kwargs)

    @print_response
    @decrypt_message.with_key
    @send_securily.with_key
    def get_all_files(self, *args, **kwargs):
        print('getting all files')
        return requests.get(self.files_address, **kwargs)

    @print_response
    @decrypt_message.with_key
    @send_securily.with_key
    def get_file(self, *args, **kwargs):
        print('getting file')
        return requests.get(self.file_address, **kwargs)

    @print_response
    @decrypt_message.with_key
    @send_securily.with_key
    def add_file(self, *args, **kwargs):
        print('add file')
        return requests.post(self.files_address, **kwargs)

    @print_response
    @decrypt_message.with_key
    @send_securily.with_key
    def edit_file(self, *args, **kwargs):
        print('edit file')
        return requests.put(self.file_address, **kwargs)

    @print_response
    @decrypt_message.with_key
    @send_securily.with_key
    def del_file(self, *args, **kwargs):
        print('deleting')
        return requests.delete(self.file_address, **kwargs)
