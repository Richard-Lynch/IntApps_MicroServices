#!/bin/bash

V1=$1

json_template='{
    name: $v1
}'
address="http://127.0.0.1:8080"
jq -n --arg v1 "$V1" "$json_template" |
    curl -i -X POST \
    -H "Content-Type: application/json" \
    -d@- \
    "$address"/pals
