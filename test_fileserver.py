#!/usr/local/bin/python3

import os
import fileserver
import unittest
import tempfile
from flask import Flask, jsonify, request
import json
class fileserverTestCase(unittest.TestCase):
    def setUp(self):
        self.app = fileserver.app.test_client()
        # self.db_fd, fileserver.app.config['DATABASE'] = tempfile.mkstemp()
        # fileserver.app.testing = True
        # self.app = fileserver.app.test_client()
        # with fileserver.app.app_context():
            # fileserver.init_db()

    def tearDown(self):
        pass
        # os.close(self.db_fd)
        # os.unlink(fileserver.app.config['DATABASE'])
    
    def test_root(self):
        rv = self.app.get('/')
        # print (rv.data)
        assert b'"test": "success!"' in rv.data
    
    def test_get_pals(self):
        rv = self.app.get('/pals')
        # print (rv.data)
        # assert b'"name": "Richie"' in rv.data
        assert b'"name": "Ali"' in rv.data
        assert b'"name": "Jenny"' in rv.data
        assert b'"name": "Ste"' in rv.data
    
    def test_get_pal(self):
        rv = self.app.get('/pals/Ali')
        # print (rv.data)
        assert b'"name": "Ali"' in rv.data
        assert b'"name": "Jenny"' not in rv.data
    
    def test_get_pal_no(self):
        rv = self.app.get('/pals/Alixx')
        # print (rv.data)
        assert b'"error": "Not found"' in rv.data

    def test_create_pal(self):
        rv = self.app.post('/pals', data=json.dumps(dict(name='Fionn')), content_type='application/json', follow_redirects=True)
        # print (rv.data)
        assert b'"id":' in rv.data
        assert b'"name": "Fionn"' in rv.data

    def test_create_pal_no_name(self):
        rv = self.app.post('/pals', data=json.dumps(dict(namre='Fionn')), content_type='application/json', follow_redirects=True)
        # print (rv.data)
        assert b'"error": "Bad request"' in rv.data

    def test_create_pal_not_json(self):
        rv = self.app.post('/pals', data=dict(namre='Fionn'), follow_redirects=True)
        # print (rv.data)
        assert b'"error": "Bad request"' in rv.data

    def test_update_pal(self):
        rv = self.app.put('/pals/3', data=json.dumps(dict(name='Stephen')), content_type='application/json', follow_redirects=True)
        # print (rv.data)
        assert b'"name": "Stephen"' in rv.data
    def test_update_pal_no_name(self):
        rv = self.app.put('/pals/3', data=json.dumps(dict(naxme='Stephen')), content_type='application/json', follow_redirects=True)
        # print (rv.data)
        assert b'"name": "Stephen"' in rv.data
    def test_update_pal_doesnt_exist(self):
        rv = self.app.put('/pals/7', data=json.dumps(dict(name='Stephen')), content_type='application/json', follow_redirects=True)
        # print (rv.data)
        assert b'"error": "Not found"' in rv.data
    def test_update_pal_not_json(self):
        rv = self.app.put('/pals/3', data=dict(name='Stephen'), follow_redirects=True)
        # print (rv.data)
        assert b'"error": "Bad request"' in rv.data
    def test_update_pal_name_not_string(self):
        rv = self.app.put('/pals/3', data=json.dumps(dict(name=1)), content_type='application/json', follow_redirects=True)
        # print (rv.data)
        assert b'"error": "Bad request"' in rv.data
    def test_delete_pal(self):
        rv = self.app.delete('/pals/0', follow_redirects=True)
        # print (rv.data)
        assert b'"result": true' in rv.data
        rv = self.app.get('/pals')
        # print (rv.data)
        assert b'"name": "Richie"' not in rv.data

if __name__ == '__main__':
    unittest.main()
