#!/usr/local/bin/python3
from client_lib import DFS_client

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
print("GETTING")
r = cli.get_all_files()
# try:
#     files = r.json()['files']
#     for f in files:
#         print("GETTING 1")
#         cli.get_file(f['uri'])
# except Exception as e:
#     print('error', e)
# r = cli.search_for_file(**{'name': 'test.txt'})
