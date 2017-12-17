#!/usr/local/bin/python3
from client_lib import DFS_client
from bson.objectid import ObjectId
from pprint import pprint


def test_setup():
    global cli
    cli = DFS_client('admin', 'admin')
    print('CREATEING RICHIE')
    cli.create_user(**{
        'username': 'richie',
        'password': 'pass',
        'admin': False
    })
    cli = DFS_client('richie', 'pass')
    print('GENERATING TOKEN')
    cli.generate_token()
    print('CHECKING AUTH')
    cli.check_auth()

    print('TESTING TEMP')
    cli2 = DFS_client('temp', 'nah')
    print('CHECKING AUTH')
    cli2.check_auth()

    print("GETTING")
    cli.get_all_files()


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
        if r['status'] == 200:
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

    print('TRYING GOOD EDITS')
    try:
        if r['status'] == 200:
            msg = r['message']
            files = msg['files']
            for f in files:
                f['content'] = 'please no!'
                cli.edit_file(**f)
    except Exception as e:
        print('error', e)

    print('TRYING BAD EDITS')
    try:
        if r['status'] == 200:
            msg = r['message']
            files = msg['files']
            for f in files:
                f['content'] = 'please yes!'
                cli.edit_file(**f)
    except Exception as e:
        print('error', e)

    print('checking edits')
    try:
        if r['status'] == 200:
            print('r')
            print(r)
            msg = r['message']
            files = msg['files']
            print('files')
            pprint(files)
            for f in files:
                print('getting file')
                print(f)
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
        if r['status'] == 200:
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
        if r['status'] == 200:
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
    test_adding()
    test_get_all()
    test_search()
    test_edits()
    # test_lock()
    test_delete()
