#!/bin/bash

./reg_file.sh "test.txt" "1" "demo_uri_1"
./reg_file.sh "test.txt" "2" "demo_uri_2"
./reg_file.sh "demo.txt" "2" "demo_uri_2"
./reg_file.sh "test.txt" "3" "demo_uri_3"
./reg_file.sh "test.txt" "3" "demo_uri_4"
./search_file.sh "test.txt"
./search_file.sh "demo.txt"
