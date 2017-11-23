#!/bin/bash

if [[ $# != 2 ]] ; then
    echo "takes exactly 2 args: name content"
    exit
fi

V1=$1
V2=$2

json_template='{
    name: $v1,
    content: $v2
}'

address="http://127.0.0.1:8080"
jq -n --arg v1 "$V1" \
    --arg v2 "$V2" "$json_template" |
    curl -i -X POST \
    -H "Content-Type: application/json" \
    -d@- \
    "$address"/files
