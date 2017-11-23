#!/usr/local/bin/python3
from flask_restful import fields
# ----- fields -----
def init_fields(machine_id):
    global file_summary_fields
    global file_fields
    global file_list_fields
    global register_fields
    file_summary_fields = {
        'name': fields.String,
        'id': fields.Integer,
        'machine' : fields.Integer(default=machine_id),
        'uri': fields.Url('file', absolute=True),
        'https_uri': fields.Url('file', absolute=True, scheme='https')
    }
    file_fields = {
        'name': fields.String,
        'id': fields.Integer,
        'machine' : fields.Integer(default=machine_id),
        'uri': fields.Url('file', absolute=True),
        'https_uri': fields.Url('file', absolute=True, scheme='https'),
        'content': fields.String
    }
    file_list_fields={
            'files' : fields.Nested(file_fields)
        }
    register_fields = {
        'name': fields.String,
        'machine_id' : fields.Integer(default=machine_id),
        'uri': fields.Url('files', absolute=True),
        }
