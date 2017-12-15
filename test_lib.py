#!/usr/local/bin/python3
from client_lib import DFS_client
from bson.objectid import ObjectId

cli = DFS_client('richie', 'pass')
# print(type(cli))
cli.create_user('admin', 'admin', 'richie', 'pass')
cli.check_auth()
cli.generate_token()
print("GETTING")
cli.get_all_files()

print("ADDING")
cli.add_file(name='test.txt', content='hello world')
cli.add_file(name='test2.txt', content='goobye world')

print("GETTING")
r = cli.get_all_files()

print('tryign to get all files')
try:
    if r['code'] == 200:
        msg = r['message']
        files = msg['files']
        for f in files:
            cli.get_file(**{'_id': f['_id']})
except Exception as e:
    print('error', e)

print('tryign to edit all files')
try:
    if r['code'] == 200:
        msg = r['message']
        files = msg['files']
        for f in files:
            cli.edit_file(**{
                '_id': f['_id'],
                'content': 'please no!',
                'name': None
            })
except Exception as e:
    print('error', e)

print('checking edits')
try:
    if r['code'] == 200:
        msg = r['message']
        files = msg['files']
        for f in files:
            cli.get_file(**{'_id': f['_id']})
except Exception as e:
    print('error', e)

print('searching for file')
cli.search_for_file(**{'name': 'test.txt'})

print('tryign to delete all files')
try:
    if r['code'] == 200:
        msg = r['message']
        files = msg['files']
        for f in files:
            cli.del_file(**{'_id': f['_id']})
except Exception as e:
    print('error', e)
print("GETTING")
r = cli.get_all_files()
