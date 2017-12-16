#!/Users/richie/miniconda3/bin/python3
from collections import defaultdict
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)
import requests
from pprint import pprint


def encrypt_message(message, key):
    s = Serializer(key)
    return s.dumps(message).decode()


def make_request(rtype, address):
    def make_specific_request(key, *args, **kwargs):
        message = {k: v for k, v in kwargs.items()}
        message = encrypt_message(message, key)
        print('message', message)
        if len(args) > 0:
            send_to = args[0]
            print('path', send_to)
        else:
            send_to = address
            print('address', send_to)
        r = rtype(send_to, json={'token': token.decode(), 'message': message})
        print('r', r)
        j = r.json()
        print('j')
        pprint(j)
        return j

    return make_specific_request


def make_all_requests(rtypes, addresses):
    all_requests = defaultdict(dict)
    for ka, va in addresses.items():
        for krt, vrt in rtypes.items():
            all_requests[ka][krt] = make_request(vrt, va)
    return all_requests


rtypes = {
    'get': requests.get,
    'post': requests.post,
    'put': requests.put,
    'delete': requests.delete,
}
addresses = {
    'file_server': file_address,
    'auth_server': auth_address,
    'demo_server': demo_address,
}
username = 'Richie'
password = 'password'
auth_address = 'http://127.0.0.1:8083/auth'
demo_address = 'http://127.0.0.1:8085/token'
file_address = 'http://127.0.0.1:8080/files'
my_requests = make_all_requests(rtypes, addresses)
