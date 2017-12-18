# A Distributed File System using REST
## Internet Applications / Scaleable Computing

### Overview 
This project aimed to deliver a simple distributed file system, to specifications provided. 

#### 1. Distributed Transparent File Access (File Server)
The file server is the backbone of this system, providing basic file interactions.
It provides two endpoints; File and Files.
#### File
Call | Purpose
---- | ----
get() | Retrieve a file
post() | Add a new file
put() | Edit an exisiting file
delete() | Delete an existing file
#### Files
Call | Purpose
---- | ----
get() | Retrieve a list of all files
delete() | Shutdown file server

2. Security Service (Auth Server)
3. Directory Service (Dir Server)
4. Locking Service (Lock Server)
5. Caching Service (Built into library)
6. Client Library (Client lib)



