#!/bin/bash
command="127.0.0.1:8080/"
if [[ $# > 0 ]] ; then
    command="$command$1"
fi
if [[ $# > 1 ]] ; then
    command="$command/$2"
fi
if [[ $# > 2 ]] ;  then
    command="$command/$3"
fi

echo $command
curl -i $command 
