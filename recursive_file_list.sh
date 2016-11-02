#!/usr/bin/env bash
find $1 -type f -printf "%P\t%s\t%A@\t%C@\t%T@\n"
