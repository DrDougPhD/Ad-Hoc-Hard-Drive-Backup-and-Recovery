#!/usr/bin/env bash
#
# Build a list of duplicate files stored within a directory.
#
# Copyright 2016 Doug McGeehan. All rights reserved.
#
#------------------------------------------------------------------------------
#
# TODO:
#  Absolute paths for each duplicate file
#  File groups sorted by size
#  Replace a duplicate file with a symbolic link of the same name
#  Obtain user/group, creation times, modification times of files
#  Sort files within group by date, from oldest to newest
#
echo "Current working directory: $(pwd)"
echo "------------------------------------------------------------------------"
fdupes --recurse --size "$1"
