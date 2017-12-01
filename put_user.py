#!/usr/local/bin/python3

if [[ $# != 2 ]] ; then
    echo "takes exactly 2 args: uri conent"
    exit
fi

V1="$1"
V2="$2"

json_template='{
    username: $v1,
    password: $v2
}'

address="http://127.0.0.1:8083/auth"
jq -n --arg v1 "$V1" \
    --arg v2 "$V2" "$json_template" |
    curl -i -X PUT \
    -H "Content-Type: application/json" \
    -d@- \
    "$1"
    # "$address/files/$V1"
