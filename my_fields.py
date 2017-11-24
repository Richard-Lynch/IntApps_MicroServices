#!/usr/local/bin/python3
from flask_restful import fields
# ----- fields -----
file_summary_fields = {
    'name': fields.String,
    'id': fields.Integer,
    'machine_id' : fields.Integer(default=-1),
    'uri': fields.Url('file', absolute=True),
    'https_uri': fields.Url('file', absolute=True, scheme='https')
}
file_fields = {
    'name': fields.String,
    'id': fields.Integer,
    'machine_id' : fields.Integer(default=-1),
    'uri': fields.Url('file', absolute=True),
    'https_uri': fields.Url('file', absolute=True, scheme='https'),
    'content': fields.String
}
file_list_fields={
        'files' : fields.Nested(file_fields)
    }
register_fields = {
    'name': fields.String,
    'machine_id' : fields.Integer(default=-1),
    'uri': fields.Url('files', absolute=True),
    }
