#!/usr/local/bin/python3
from client_lib import DFS_client
from bson.objectid import ObjectId

cli = DFS_client('richie', 'pass')
# print(type(cli))
cli.create_user('admin', 'admin', 'richie', 'pass')
cli.check_auth()
cli.generate_token()
# cli.seach_for_file('test')
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
print('tryign to delete all files')
try:
    if r['code'] == 200:
        msg = r['message']
        files = msg['files']
        for f in files:
            cli.del_file(**{'_id': f['_id']})
except Exception as e:
    print('error', e)
r = cli.get_all_files()
