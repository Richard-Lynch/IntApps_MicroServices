#!/usr/local/bin/python3
from flask_restful import fields

"""Provides fields to be used with flask_restful.marshal"""

class Objectid(fields.Raw):
    """Custom field, to typecase ObjectId as str"""
    def format(self, value):
        return str(value)


# ----- fields -----
file_summary_fields = {
    'name': fields.String,
    'machine_id': fields.String(default=-1),
    '_id': Objectid(default='000000000000000000000000'),
    'version': fields.Integer(default=-100),
    'uri': fields.Url('file', absolute=True),
    'https_uri': fields.Url('file', absolute=True, scheme='https')
}
file_fields = {
    'name': fields.String,
    'machine_id': fields.String(default=-1),
    '_id': Objectid(default='000000000000000000000000'),
    'version': fields.Integer(default=-100),
    'uri': fields.Url('file', absolute=True),
    'https_uri': fields.Url('file', absolute=True, scheme='https'),
    'content': fields.String
}
file_list_fields = {'files': fields.Nested(file_fields)}
register_fields = {
    'name': fields.String,
    'machine_id': fields.String(default=-1),
    'uri': fields.Url('file', absolute=True),
}
register_machine_fields = {'callback': fields.String}
registered_machine_fields = {
    '_id': Objectid(default='000000000000000000000000'),
}
registered_fields = {
    'name': fields.String,
    'machine_id': fields.String(default=-1),
    'reg_id': Objectid(attribute='_id'),
    'reg_uri': fields.Url('register', absolute=True),
}
dir_file_fields = {
    'name': fields.String,
    'machine_id': fields.String,
    'uri': fields.String,
}
