#!/bin/bash

if [[ $# == 2 ]] ; then
    command="$1"
    V1=$2
elif [[ $# == 3 ]] ; then
    command="$1/$2"
    V1=$3
elif [[ $# == 4 ]] ;  then
    command="$1/$2/$3"
    V1=$4
else
    exit
fi

json_template='{
    name: $v1
}'
address="http://127.0.0.1:8080"
jq -n --arg v1 "$V1" "$json_template" |
    curl -i -X PUT \
    -H "Content-Type: application/json" \
    -d@- \
    "$address"/"$command"
