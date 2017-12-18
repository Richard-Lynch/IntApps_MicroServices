# A Distributed File System using REST
## Internet Applications / Scaleable Computing

### Overview 
This project aimed to deliver a simple distributed file system, to specifications provided. 

#### 1. Distributed Transparent File Access (File Server)
The file server is the backbone of this system, providing basic file interactions.
It provides two endpoints; File and Files.
#### File
To act on an single file.

Call | Purpose
---- | ----
get() | Retrieve a file
post() | Add a new file
put() | Edit an exisiting file
delete() | Delete an existing file

#### Files
To act on the server

Call | Purpose
---- | ----
get() | Retrieve a list of all files
delete() | Shutdown file server

#### 2. Security Service (Auth Server)
The auth server is used for all authenicated communications in this system. It acheives this by having a list of users (either admin or not) who can generate a token with the auth server (using their credentials) which can then be used for interactions with all other services in the system. This is achieved using 3 key mutual encryption, allowing the client to verify the indentity of any service it communicates with, and vice versa. 
It provides  one endpoint; Auth.
#### Auth
To become authorized or create new users if admin.

Call | Purpose
---- | ----
get() | Check client authorization level
post() | Create a new user (if admin)
put() | Generate a new token, using credentials

#### 3. Directory Service (Dir Server)
The dir server acts as a way of finding the locaiton of files within the system. Each file is registered with the dir server, which is then able to queried to find the location of any given file on the systems.
It provides two endpoints; Search and Register.
#### Search
Allows the client to search for a file by name

Call | Purpose
---- | ----
get() | Search for a file by name

#### Register
Allows machines to register and to register files.

Call | Purpose
---- | ----
get() | Register a new service with the directory server
post() | Register a new file with the directory server
put() | Un-register a file with the directory server
delete() | Un-register a machine with the directory server

#### 4. Locking Service (Lock Server)
The lock server acts as a sepmaphore between clients in the system, allowing them, to ensure exclusive access to a file.
It provides one endpoint; Lock
#### Lock
Allows the client to interact with locks.

Call | Purpose
---- | ----
get() | Retrieve lock status of file.
post() | Lock a file
delete() | Unlock a file

#### 5. Caching Service (Built into library)
Caching is built into the client libary itself, and attempts to reduce network traffic and retrieval times by keeping a local copy of files, which is returned rather than re-requesting the file from the server.

#### 6. Client Library (Client lib)
The client library provides funcions to interact with the file system, allowing for language specific calls to be made.



