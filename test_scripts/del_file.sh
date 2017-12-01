#!/bin/bash

if [[ $# != 1 ]] ; then
    echo "takes exactly 1 arg: id"
    exit
fi

V1="$1"
address="http://127.0.0.1:8080"
    curl -i -X DELETE \
    "$address"/files/$V1
