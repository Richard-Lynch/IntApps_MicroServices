#!/usr/local/bin/python3
# ----- Errors -----
errors = {
        'not_found' : {
            'message' : "Not Found",
            'status' : 404,
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

class not_found(HTTPException):
    code = 400
class bad_request(HTTPException):
    code = 400
class unauthorized(HTTPException):
    code = 400
