#!/usr/bin/env bash

# remove a dangling forward slash from directory
#DIRECTORY=$(echo "$1" | sed 's,/$,,g') 
DIRECTORY="$1"

find "$DIRECTORY" -type f -printf "%P\t%s\t%A@\t%C@\t%T@\n"
