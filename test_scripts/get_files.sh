#!/bin/bash
command="127.0.0.1:"
port="8080"
endpoint="/files"
if [[ $# == 1 ]] ; then
    port="$1"
fi
echo $command$port$endpoint
curl -i $command$port$endpoint
