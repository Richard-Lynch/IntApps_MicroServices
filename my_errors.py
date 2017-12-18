#!/usr/local/bin/python3
"""
This module provides HTTPException classses which can be raised

To add an error, add its name, message and status to the dict
'errors' below

To include; 
    import my_errors
    my_errors.make_classes(my_errors.errors)

"""

# ----- Errors -----
from flask_restful import HTTPException
errors = {
    'not_found': {
        'message': "Not Found",
        'status': 404,
    },
    'user_not_found': {
        'message': 'User Not Found',
        'status': 404,
    },
    'user_exists': {
        'message': 'User already exists',
        'status': 400,
    },
    'file_exists': {
        'message': 'File already exists',
        'status': 400,
    },
    'bad_request': {
        'message': 'Bad Request',
        'status': 400,
    },
    'unauthorized': {
        'message': 'Unauthorized Access',
        'status': 403,
    },
    'unauthorized_bad_sig': {
        'message': 'Unauthorized Access: Bad Signature',
        'status': 403,
    },
    'unauthorized_sig_expired': {
        'message': 'Unauthorized Access: Signature Expired',
        'status': 403,
    },
    'unauthorized_user_not_found': {
        'message': 'Unauthorized Access: User not found',
        'status': 403,
    },
    'unauthorized_bad_password': {
        'message': 'Unauthorized Access: Bad password',
        'status': 403,
    },
    'unauthorized_bad_request': {
        'message': 'Unauthorized Access: Bad request',
        'status': 403,
    },
}


def make_classes(errors):
    """Generate the error classes"""
    for key in errors:
        globals()[key] = type(key, (HTTPException, ), {'code': 400})
