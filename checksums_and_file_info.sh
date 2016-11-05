#!/usr/bin/env bash
#
# Iterate over all files stored within a directory, collecting their checksums
# and other file information.
#
# Usage: <blah>.sh < files,sizes.txt > files,sizes,checksums.txt
#
# Copyright 2016 Doug McGeehan. All rights reserved.
#
#------------------------------------------------------------------------------
#
# TODO:
#  Given a files containing urls and file sizes, only compute the md5sums
#    of those files with matching sizes.
#  Given two files containing urls and files sizes, only compute the md5sums
#    of those files with matching sizes.
#

# The input to this script is a list of file paths and file sizes.
# Assume the first column is the path of a file, and the second column is the
# file's size in bytes. Columns are separated by tabs. All other columns are
# ignored.
while read line
do
  echo "$line"
done < /dev/stdin


#### stashed ####
#find $1 -type f -printf "%P\t%s\t%A@\t%C@\t%T@\n"
# execute md5sum on each file found
#find . -exec grep chrome {} \;
