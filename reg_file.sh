#!/bin/bash

if [[ $# != 3 ]] ; then
    echo "takes exactly 3 args: name, machine_id, uri"
    exit
fi

V1="$1"
V2="$2"
V3="$3"

json_template='{
    name: $v1,
    machine_id: $v2,
    uri: $v3
}'

address="http://127.0.0.1:8081"
jq -n \
    --arg v1 "$V1" \
    --arg v2 "$V2" \
    --arg v3 "$V3" \
    "$json_template" |
    curl -i -X PUT \
    -H "Content-Type: application/json" \
    -d@- \
    "$address/dirs/register"
