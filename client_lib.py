#!/Users/richie/miniconda3/bin/python3

import requests


def print_requests_response(f):
    def wrapped_f(*args, **kwargs):
        r = f(*args, **kwargs)
        print('response:', r)
        print('json', r.json())
        return r


class DFS_client():
    def __init__(self, username, password):
        self.auth_address = 'http://127.0.0.1:8080/auth'
        self.file_address = 'http://127.0.0.1:8082/files'
        self.dir_address = 'http://127.0.0.1:8081/dir'
        self.username = username
        self.password = password

    @print_requests_response
    def create_user(self, admin_username, admin_password, username, password):
        r = requests.post(
            self.auth_address,
            json={'username': username,
                  'password': password},
            auth=(admin_username, admin_password))
        return r
