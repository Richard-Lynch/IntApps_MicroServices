#!/bin/bash
command="127.0.0.1:8081/files"
if [[ $# == 1 ]] ; then
    command="$command/$1"
fi
echo $command
curl -i $command
