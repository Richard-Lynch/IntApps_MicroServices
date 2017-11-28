#!/bin/bash

if [[ $# != 1 ]] ; then
    echo "takes exactly 1 args: machine_id"
    exit
fi

V1="$1"

json_template='{
    machine_id: $v1,
}'

address="http://127.0.0.1:8081"
jq -n \
    --arg v1 "$V1" \
    "$json_template" |
    curl -i -X DELETE \
    -H "Content-Type: application/json" \
    -d@- \
    "$address/dirs/register"
