#!/usr/local/bin/python3
from client_lib import DFS_client
from bson.objectid import ObjectId


def test_setup():
    global cli
    cli = DFS_client('admin', 'admin')
    cli.create_user(**{
        'username': 'richie',
        'password': 'pass',
        'admin': False
    })
    cli = DFS_client('richie', 'pass')
    cli.generate_token()
    cli.check_auth()
    cli2 = DFS_client('temp', 'nah')
    cli2.check_auth()

    # print("GETTING")
    # cli.get_all_files()


def test_adding():
    print("ADDING")
    cli.add_file(name='test.txt', content='hello world')
    cli.add_file(name='test2.txt', content='goobye world')


def test_get_all():
    global r
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


def test_edits():
    global r
    print("GETTING")
    r = cli.get_all_files()

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


def test_search():
    print('searching for files')
    cli.search_for_file(**{'name': 'test.txt'})


def test_delete():
    global r
    print("GETTING")
    r = cli.get_all_files()

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


def test_lock():
    global r
    print("GETTING")
    r = cli.get_all_files()

    print('tring to lock all files')
    try:
        if r['code'] == 200:
            msg = r['message']
            files = msg['files']
            print('CHECKING')
            for f in files:
                cli.check_lock_file(**{'uri': f['uri'], '_fid': f['_id']})
            print("LOCKING")
            for f in files:
                cli.lock_file(**{'uri': f['uri'], '_fid': f['_id']})
            print('CHECKING')
            for f in files:
                cli.check_lock_file(**{'uri': f['uri'], '_fid': f['_id']})
            print('LOCKING')
            for f in files:
                cli.lock_file(**{'uri': f['uri'], '_fid': f['_id']})
            print('CHECKING')
            for f in files:
                cli.check_lock_file(**{'uri': f['uri'], '_fid': f['_id']})
            print('UNLOCKING')
            for f in files:
                cli.unlock_file(**{'uri': f['uri'], '_fid': f['_id']})
            print('CHECKING')
            for f in files:
                cli.check_lock_file(**{'uri': f['uri'], '_fid': f['_id']})
    except Exception as e:
        print('error', e)


if __name__ == "__main__":
    test_setup()
    # test_adding()
    # test_get_all()
    # test_search()
    # test_edits()
    # test_lock()
    # test_delete()
