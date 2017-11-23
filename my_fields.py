#!/usr/local/bin/python3

# ----- fields -----
file_summary_fields = {
    'name': fields.String,
    'id': fields.Integer,
    'uri': fields.Url('file', absolute=True),
    'https_uri': fields.Url('file', absolute=True, scheme='https')
}
file_fields = {
    'name': fields.String,
    'id': fields.Integer,
    'uri': fields.Url('file', absolute=True),
    'https_uri': fields.Url('file', absolute=True, scheme='https'),
    'content': fields.String
}
file_list_fields={
        'files' : fields.Nested(file_fields)
    }
register_fields = {
    'name': fields.String,
    'machine_id' : fields.Integer(default=fileS.machine_id),
    'uri': fields.Url('files', absolute=True),
    }
