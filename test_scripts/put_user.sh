#!/bin/bash

if [[ $# != 2 ]] ; then
    echo "takes exactly 2 args: username password"
    exit
fi

address="http://127.0.0.1:8083/auth"
    curl \
    -u "$1:$2" \
    -X PUT \
    "$address"
