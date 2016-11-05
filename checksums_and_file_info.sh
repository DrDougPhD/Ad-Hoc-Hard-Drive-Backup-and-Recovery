#!/usr/bin/env bash
#
# Intelligent checksums and duplicate detection. Iterate over all files,
# collecting their checksums and other file information only for files that
# share the same size. The motivation of this script is to put as little burden
# on the hard drive(s) containing those files.
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
sort --field-separator=$'\t' --key=2 --numeric-sort /dev/stdin

# build associative array of bytes => [filepaths]
# remove singletons - e.g. 123 -x-> ['/tmp/file.txt']
#                          124 ---> ['/tmp/f1.txt', '/tmp/f2.txt']
# for each mapping, compute the md5sums of the files
# sort files within each mapping by file's age
# obtain more info on files, including timestamps, owner/group, etc
# output to file

#awk -F"\t" '{print $1}' /dev/stdin
 
#### stashed ####
#find $1 -type f -printf "%P\t%s\t%A@\t%C@\t%T@\n"
# execute md5sum on each file found
#find . -exec grep chrome {} \;
