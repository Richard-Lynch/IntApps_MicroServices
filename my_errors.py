#!/usr/local/bin/python3
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
    classes = []
    for key in errors:
        d = {}
        d['code'] = 400
        myClass = type(key, (HTTPException, ), d)
        globals()[key] = myClass
        classes.append(myClass)
    return classes


# make_classes(errors)
# class not_found(HTTPException):
#     code = 400
# class user_not_found(HTTPException):
#     code = 400
# class bad_request(HTTPException):
#     code = 400
# class unauthorized(HTTPException):
#     code = 400
