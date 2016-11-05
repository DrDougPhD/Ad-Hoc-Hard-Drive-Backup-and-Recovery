#!/usr/bin/env bash

# remove a dangling forward slash from directory
DIRECTORY=$(echo "$1" | sed 's,/$,,g') 

find "$DIRECTORY" -type f -printf "'${DIRECTORY}/%P'\t%s\t%A@\t%C@\t%T@\n"
