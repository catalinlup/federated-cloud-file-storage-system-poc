#!/bin/bash

BASE_LOG_PATH="./data/logs"

while getopts ":t:u:p:l:" opt; do
  case $opt in
    t)
      arg_target="$OPTARG"
      ;;
    u)
      arg_user="$OPTARG"
      ;;
    p)
      arg_path="$OPTARG"
      ;;
    l)
      arg_log="$OPTARG"
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done



python3 app.py $arg_target --user $arg_user --path $arg_path &> cool.txt