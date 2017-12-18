#!/Users/richie/miniconda3/bin/python3

from collections import defaultdict
import requests
import send_securily
import decrypt_message
import cache
import catch
import print_
from pprint import pprint


def auth(f):
    """Decorator to wrap interation will all servers but AuthServer"""
    # print the response code and json
    @print_.response
    # catch ConnectionError if server is down
    @catch.dead
    # decrypt response from server with key
    @decrypt_message.with_key
    # encrypt outgoing message with key
    @send_securily.with_key
    def wrapped_f(*args, **kwargs):
        return f(*args, **kwargs)

    return wrapped_f


class DFS_client():
    """Client for distributed file system"""

    def __init__(self, username, password):
        # print('creating user')
        self.username = username
        self.password = password
        self.key = password
        self.token = password.encode()
        self.public_key = 'this simulates a public private key pair'
        self.get_addresses()
        self.cached_files = defaultdict(dict)
        self.cached_files_list = []
        self.cached_file_limit = 20

    # interal funcs
    def get_addresses(self):
        """Retrieve addresses for each server"""
        # this should call registry server
        # print('getting addresses')
        self.auth_address = 'http://127.0.0.1:8083/auth'
        self.files_address = 'http://127.0.0.1:8080/files'
        self.file_address = 'http://127.0.0.1:8080/file'
        self.dir_address = 'http://127.0.0.1:8081/dirs'
        self.lock_address = 'http://127.0.0.1:8084/lock'

    def extract_token(f):
        """Decorator to extract the key and token from generate token"""

        def wrapped_f(self, *args, **kwargs):
            # print('extracting')
            r = f(self, *args, **kwargs)
            try:
                self.token = r['message']['token'].encode()
                self.key = r['message']['key']
            except KeyError:
                # print('Key error getting token')
                raise
            return r

        return wrapped_f

    def add_to_cache(self, file_data):
        """Add a file to cache, or update a cached copy"""
        # print('adding to cache')
        # check if the cache is full
        if len(self.cached_files_list) > self.cached_file_limit:
            del self.cached_files[self.cached_files_list.pop(0)['_id']]
        # create a new cached copy by merging the old and new
        Id = file_data['_id']
        new_file = {
            **self.cached_files[Id],
            **{k: v for k, v in file_data.items() if v is not None}}
        self.cached_files[Id] = new_file
        self.cached_files_list.append(new_file)

    def get_from_cache(self, _id):
        """Retreive a cached copy of a file"""
        # print('getting from cache')
        cached_file = self.cached_files[_id]
        self.cached_files_list.append(
            self.cached_files_list.pop(
                self.cached_files_list.index(cached_file)))
        return cached_file

    # --- Authorization ---
    @print_.response
    @catch.dead
    @decrypt_message.with_key
    @send_securily.with_credentials
    def create_user(self, *args, **kwargs):
        """Create a new user. Requires admin"""
        # print('createing user')
        r = requests.post(self.auth_address, **kwargs)
        return r

    # auth utils
    @print_.response
    @catch.dead
    @decrypt_message.with_password
    @send_securily.with_credentials
    def check_auth(self, *args, **kwargs):
        """Check client authorization level"""
        # print('checking auth')
        r = requests.get(self.auth_address, **kwargs)
        return r

    @print_.response
    @catch.dead
    @extract_token
    @decrypt_message.with_password
    @send_securily.with_credentials
    def generate_token(self, *args, **kwargs):
        """Generae a token for use in server communication"""
        # print('generating token')
        r = requests.put(self.auth_address, **kwargs)
        return r

    # --- Server Communication ---
    @auth
    def search_for_file(self, *args, **kwargs):
        """Search for file locations via Dir Server"""
        # print('searching for file')
        return requests.get(self.dir_address + '/search', **kwargs)

    @auth
    def get_all_files(self, *args, **kwargs):
        """Retrieve list of all files in a particular file server"""
        # print('getting all files')
        return requests.get(self.files_address, **kwargs)

    @cache.check
    @auth
    def get_file(self, *args, **kwargs):
        """Retrieve a specific file from a file server"""
        # print('getting file')
        return requests.get(self.file_address, **kwargs)

    @cache.update_on_add
    @auth
    def add_file(self, *args, **kwargs):
        """Add a file to a to a file server"""
        # print('add file')
        return requests.post(self.file_address, **kwargs)

    @cache.update_on_edit
    @auth
    def edit_file(self, *args, **kwargs):
        """Edit a specific file on a file server"""
        # print('edit file')
        return requests.put(self.file_address, **kwargs)

    @auth
    def del_file(self, *args, **kwargs):
        """Delete a specific file from a file server"""
        # print('deleting')
        return requests.delete(self.file_address, **kwargs)

    @auth
    def lock_file(self, *args, **kwargs):
        """Lock a specific file with lock server"""
        # print('lock')
        return requests.post(self.lock_address, **kwargs)

    @auth
    def unlock_file(self, *args, **kwargs):
        """Unlock a specific file with lock server"""
        # print('unlock')
        return requests.delete(self.lock_address, **kwargs)

    @auth
    def check_lock_file(self, *args, **kwargs):
        """Retrieve the lock status of specfic file with lock server"""
        # print('check lock')
        return requests.get(self.lock_address, **kwargs)
