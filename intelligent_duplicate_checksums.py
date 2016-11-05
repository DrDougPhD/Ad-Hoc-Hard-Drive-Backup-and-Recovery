#!/usr/bin/env python3

"""
Intelligent checksums and duplicate detection. Iterate over all files,
 collecting their checksums and other file information only for files that
 share the same size. The motivation of this script is to put as little burden
 on the hard drive(s) containing those files.

 Usage: <blah>.sh < files,sizes.txt > files,sizes,checksums.txt

Copyright 2016 Doug McGeehan. All rights reserved.

-------------------------------------------------------------------------------

TODO:
  Given a files containing urls and file sizes, only compute the md5sums
    of those files with matching sizes.
  Given two files containing urls and files sizes, only compute the md5sums
    of those files with matching sizes.
"""

import sys
import panda
import numpy


if __name__ == "__main__":
	"""
	The input to this script is a list of file paths and file sizes.
	Assume the first column is the path of a file, and the second column is the
	file's size in bytes. Columns are separated by tabs. All other columns are
	ignored.
	"""
	files = pandas.read_csv(
		filepath_or_buffer=sys.argv[1],
		sep='\t',
		names=['url', 'bytes', 't1', 't2', 't3'],
		usecols=['url', 'bytes'],
		dtype={'url': str, 'bytes': numpy.uint64},
		chunksize=100,
		compression='infer',
		quotechar="'"
	)

	"""
	groupby('bytes').fn()
	Splitting the data into groups based on some criteria
	Applying a function to each group independently (if more than one, calc md5s; if one, delete)
	Combining the results into a data structure
	"""

	"""
	build associative array of bytes => [filepaths]
	remove singletons - e.g. 123 -x-> ['/tmp/file.txt']
        	                 124 ---> ['/tmp/f1.txt', '/tmp/f2.txt']
	for each mapping, compute the md5sums of the files
	sort files within each mapping by file's age
	obtain more info on files, including timestamps, owner/group, etc
	output to file
	"""
