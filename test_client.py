#!/usr/local/bin/python3
from collections import defaultdict
from flask import Flask, jsonify, request, make_response, url_for
# from flask_restful import Api, Resource, abort, HTTPException
# from flask_restful import reqparse, fields, marshal
# from lockserver import lockServer
import my_errors
my_errors.make_classes(my_errors.errors)
import my_fields
# from flask_httpauth import HTTPBasicAuth
from pprint import pprint
config = {}
config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
# from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)
import requests
import sys

s = Serializer(config['SECRET_KEY'])
username = 'Richie'
password = 'password'
auth_address = 'http://127.0.0.1:8083/auth'
demo_address = 'http://127.0.0.1:8085/token'
file_address = 'http://127.0.0.1:8080/files'


def check_auth(username, password):
    r = requests.get(auth_address, auth=(username, password))
    print(r)
    print(r.json())


def create_user(username, password):
    r = requests.post(
        auth_address,
        json={'username': username,
              'password': password},
        auth=(username, password))
    print(r)
    print(r.json())


def generate_token(username, password):
    r = requests.put(auth_address, auth=(username, password))
    print(r)
    print(r.json())
    try:
        token = r.json()['token'].encode()
        key = r.json()['key']
        return token, key
    except Exception:
        print('token not in json')
        return None


def read_token(token):
    try:
        data = s.loads(token)
        for k, v in data.items():
            print('{}: {}'.format(k, v))
            return data
    except SignatureExpired:
        print('expired')
        return None
    except BadSignature:
        print('bad')
        return None


def test_token(token, key):
    s = Serializer(key)
    message = s.dumps({'name': 'testing'}).decode()
    r = requests.get(
        demo_address, json={
            'token': token.decode(),
            'message': message
        })
    print('r', r)
    print('j', r.json())
    return True


def make_request(rtype, address):
    def encrypt_message(message, key):
        s = Serializer(key)
        return s.dumps(message).decode()

    def make_specific_request(key, *args, **kwargs):
        message = {k: v for k, v in kwargs.items()}
        message = encrypt_message(message, key)
        print('message', message)
        send_to = address
        print('address', send_to)
        if len(args) > 0:
            send_to += args[0]
            print('path', send_to)

        r = rtype(send_to, json={'token': token.decode(), 'message': message})
        return r

    return make_specific_request


def make_all_requests(addresses):
    rtypes = {
        'get': requests.get,
        'post': requests.post,
        'put': requests.put,
        'delete': requests.delete,
    }
    all_requests = defaultdict(dict)
    for ka, va in addresses.items():
        for krt, vrt in rtypes.items():
            all_requests[ka][krt] = make_request(vrt, va)
    return all_requests


addresses = {
    'file_server': file_address,
    'auth_server': auth_address,
    'demo_server': demo_address,
}
my_requests = make_all_requests(addresses)

print('checking auth before create')
check_auth(username, password)
print('creating user')
create_user(username, password)
print('checking auth after creation')
check_auth(username, password)
print('generating token')
token, key = generate_token(username, password)

print('----posting new file: auth1----')
kwargs = {'name': 'auth1.txt', 'content': 'dont store plain text'}
result = my_requests['file_server']['post'](key, **kwargs)

print('----posting new file: auth2----')
kwargs = {'name': 'auth2.txt', 'content': 'dont store plain text'}
result = my_requests['file_server']['post'](key, **kwargs)

print('----getting all files----')
result_files = my_requests['file_server']['get'](key, **kwargs)

print('----getting second file----')
try:
    file2 = result_files['files'][1]
    path = file2['uri']
    result = my_requests['file_server']['get'](key, path, **kwargs)
except Exception as e:
    print('didnt work:', e)

print('----updating second file----')
try:
    file2 = result_files['files'][1]
    path = file2['uri']
    kwargs = {'name': None, 'content': 'SERIOUSY dont store plain text'}
    result = my_requests['file_server']['put'](key, path, **kwargs)
except Exception as e:
    print('didnt work:', e)

print('----getting second file----')
try:
    file2 = result_files['files'][1]
    path = file2['uri']
    result = my_requests['file_server']['get'](key, path, **kwargs)
except Exception as e:
    print('didnt work:', e)

print('----deleting second file----')
try:
    file2 = result_files['files'][1]
    path = file2['uri']
    result = my_requests['file_server']['delete'](key, path, **kwargs)
except Exception as e:
    print('didnt work:', e)

print('----getting second file----')
try:
    file2 = result_files['files'][1]
    path = file2['uri']
    result = my_requests['file_server']['get'](key, path, **kwargs)
except Exception as e:
    print('didnt work:', e)

sys.exit()
