#!/Users/richie/miniconda3/bin/python3

from collections import defaultdict
import requests
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)

# def make_request(rtype, address):
#     def encrypt_message(message, key):
#         s = Serializer(key)
#         return s.dumps(message).decode()

#     def make_specific_request(key, *args, **kwargs):
#         message = {k: v for k, v in kwargs.items()}
#         message = encrypt_message(message, key)
#         print('message', message)
#         send_to = address
#         print('address', send_to)
#         if len(args) > 0:
#             send_to += args[0]
#             print('path', send_to)

#         r = rtype(send_to, json={'token': token.decode(), 'message': message})
#         return r

#     return make_specific_request


def send_securily(f):
    def encrypt_message(message, key):
        s = Serializer(key)
        return s.dumps(message).decode()

    def wrapped_f(self, *args, **kwargs):
        message = {k: v for k, v in kwargs.items()}
        message = encrypt_message(message, self.key)
        print('message', message)
        kwargs = {}
        kwargs['json'] = {'token': self.token.decode(), 'message': message}
        return f(*args, **kwargs)

    return wrapped_f


def print_requests_response(f):
    def wrapped_f(*args, **kwargs):
        r = f(*args, **kwargs)
        print('response:', r)
        print('json', r.json())
        return r


class DFS_client():
    def __init__(self, username, password):
        auth_address = 'http://127.0.0.1:8083/auth'
        demo_address = 'http://127.0.0.1:8085/token'
        file_address = 'http://127.0.0.1:8080/files'
        self.addresses = {
            'file_server': file_address,
            'auth_server': auth_address,
            'demo_server': demo_address,
        }

        self.auth_address = 'http://127.0.0.1:8080/auth'
        self.file_address = 'http://127.0.0.1:8082/files'
        self.dir_address = 'http://127.0.0.1:8081/dir'
        self.username = username
        self.password = password

    # admin tools
    @print_requests_response
    def create_user(self, admin_username, admin_password, username, password):
        r = requests.post(
            self.auth_address,
            json={'username': username,
                  'password': password},
            auth=(admin_username, admin_password))
        return r

    # auth utils
    @print_requests_response
    def check_auth(self, username, password):
        r = requests.get(self.auth_address, auth=(username, password))
        return r

    @print_requests_response
    def generate_token(self):
        r = requests.put(
            self.auth_address, auth=(self.username, self.password))
        try:
            token = r.json()['token'].encode()
            key = r.json()['key']
            self.token = token
            self.key = key
            return r
        except Exception:
            print('token not in json')
            return r

    @print_requests_response
    @send_securily
    def get_file(self, path, *args, **kwargs):
        return requests.get(str(path), **kwargs)
