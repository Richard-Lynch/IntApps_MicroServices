#!/bin/bash

if [[ $# != 2 ]] ; then
    echo "takes exactly 2 args: uri conent"
    exit
fi

V1="$1"
V2="$2"

json_template='{
    content: $v1
}'

# address="http://127.0.0.1:8080"
jq -n --arg v1 "$V2" "$json_template" |
    curl -i -X PUT \
    -H "Content-Type: application/json" \
    -d@- \
    "$1"
    # "$address/files/$V1"
