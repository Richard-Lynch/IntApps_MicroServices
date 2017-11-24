#!/usr/local/bin/python3
# ----- Errors -----
from flask_restful import HTTPException
errors = {
        'not_found' : {
            'message' : "Not Found",
            'status' : 404,
            },
        'user_not_found' : {
            'message' : 'ahh couldnt find the user',
            'status' : 404,
            },
        'file_exists' : { 
            'message' : 'File already exists',
            'status' : 400,
            },
        'bad_request' : {
            'message' : 'Bad Request',
            'status' : 400,
            },
        'unauthorized' : {
            'message' : 'Unauthorized Acces',
            'status' : 403,
            },
        }

def make_classes(errors):
    classes = []
    for key in errors:
        d = {}
        d['code'] = 400
        myClass = type(key, (HTTPException,), d)
        globals()[key] = myClass
        classes.append(myClass)
    return classes
make_classes(errors)
# class not_found(HTTPException):
#     code = 400
# class user_not_found(HTTPException):
#     code = 400
# class bad_request(HTTPException):
#     code = 400
# class unauthorized(HTTPException):
#     code = 400
