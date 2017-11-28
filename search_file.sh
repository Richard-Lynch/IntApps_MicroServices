#!/bin/bash

if [[ $# != 1 ]] ; then
    echo "takes exactly 1 args: name"
    exit
fi

V1="$1"

json_template='{
    name: $v1,
}'

address="http://127.0.0.1:8081"
jq -n \
    --arg v1 "$V1" \
    "$json_template" |
    curl -i -X GET \
    -H "Content-Type: application/json" \
    -d@- \
    "$address/dirs/search"
