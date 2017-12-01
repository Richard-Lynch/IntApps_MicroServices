#!/bin/bash

./post_file.sh "test.txt" "Hello World" $1
./post_file.sh "new.txt" "Goodbye World" $1
./post_file.sh "interesting.txt" "Oh my god world what are you doing" $1
./get_files.sh $1 
