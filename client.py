#!/usr/local/bin/python3
import requests
class client():
    def __init__(self):
        print ("client created")
        self.dirServerAddress = "http://127.0.0.1:8081/files"
        self.id = '0'
        with open("client_id.txt", 'r+') as f:
            id = f.readline()
            if id != None:
                self.id = id
            f.seek(0)
            f.write(str (int(self.id) + 1))
    def show_files(self):
        r = requests.get(self.dirServerAddress).json()
        print (r)
        print ("----")
        if 'files' in r:
            files = r['files']
            for fn in files:
                for f in fn:
                    for key in f:
                        print (key, f[key])
                    print ("----")
        else:
            print(r)
    def search_files(self, filename):
        r = requests.get(self.dirServerAddress +"/random", json={'name': filename}).json()
        print (r)
        print ("----")
        files = []
        if 'file' in r:
            files = r['file']
            # for fn in files
            for f in files:
                for key in f:
                    print (key, f[key])
                print ("----")
        else:
            print("error")
            print(r)
        return files
    def read_file(self, file_uri):
        r = requests.get(file_uri).json()
        # print (r)
        # print ("----")
        if 'file' in r:
            f = r['file']
            print ("name:", f['name'])
            print ("machine:", f['machine_id'])
            print ("content:", f['content'])
            print ("----")
            return (f['content'])
        return None
    def write_file(self, file_uri, new_content):
        r = requests.put(file_uri, json={'content' : new_content}).json()
        print (r)

if __name__ == "__main__":
    c = client()
    c.show_files()
    files = c.search_files("test.txt")
    for f in files:
        content = c.read_file(f['uri'])
        if content != None:
            c.write_file(f['uri'], content + "\nfile edited by client" + str(c.id))
            c.read_file(f['uri'])



