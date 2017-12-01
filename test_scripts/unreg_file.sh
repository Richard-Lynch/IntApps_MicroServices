#!/bin/bash

if [[ $# != 1 ]] ; then
    echo "takes exactly 1 args: id"
    exit
fi

address="http://127.0.0.1:8081"
    curl -i -X DELETE \
    "$address/dirs/$1"
