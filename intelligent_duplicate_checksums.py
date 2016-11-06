#!/usr/bin/env python3

"""
Intelligent checksums and duplicate detection. Iterate over all files,
 collecting their checksums and other file information only for files that
 share the same size. The motivation of this script is to put as little burden
 on the hard drive(s) containing those files.

 Usage: <blah>.sh < files,sizes.txt > files,sizes,checksums.txt

 Output:
$path	$bytes	$owner	$group	$timestamps	$md5sums

Read input csv file
Group by file size
Filter out singleton groups
Transform by md5sums
Perhaps group by md5sums now
Sort by timestamp
Output to file

Copyright 2016 Doug McGeehan. All rights reserved.

-------------------------------------------------------------------------------

TODO:
  Given a files containing urls and file sizes, only compute the md5sums
    of those files with matching sizes.
  Given two files containing urls and files sizes, only compute the md5sums
    of those files with matching sizes.
"""

import sys
import pandas
import numpy


if __name__ == "__main__":
	"""
	The input to this script is a list of file paths and file sizes.
	Assume the first column is the path of a file, and the second column is the
	file's size in bytes. Columns are separated by tabs. All other columns are
	ignored.
	"""
	all_file_info = pandas.read_table(
		filepath_or_buffer=sys.argv[1],
		names=['url', 'bytes', 'atime', 'ctime', 'mtime'],
		#usecols=['url', 'bytes'],
		dtype={
			'url': str,
			'bytes': numpy.uint64,
			'atime': numpy.float64,
			'ctime': numpy.float64,
			'mtime': numpy.float64
		},
		compression='infer',
		quotechar="'"
	)

	print("{0} raw files {0}".format('-'*20))
	print(all_file_info)


	#all_file_info.merge(right, how='inner', on=None, left_on=None, right_on=None, left_index=False, right_index=False, sort=False, suffixes=('_x', '_y'), copy=True, indicator=False)

	print("{0} size groups {0}".format('-'*20))
	print(all_file_info.groupby('bytes').groups)

	print("{0} files w/ duplicate sizes {0}".format('-'*20))
	same_sized_files = all_file_info.groupby('bytes')\
		.filter(lambda group: len(group) > 1)

	print("{0} mintimes {0}".format('-'*20))
	min_times = same_sized_files.loc[:, ['atime', 'ctime', 'mtime']].min(
		axis=1
	)

	same_sized_files.loc[:,"min_times"] = min_times
	#same_sized_files.merge(min_times, copy=False)
	#same_sized_files.loc[:, 'min_time'] = min_times

	same_sized_files.loc[:,'md5'] = same_sized_files.loc[:, 'url'].map(lambda path: path.upper())

	print(same_sized_files)

	"""
	print("{0} files w/ duplicate sizes {0}".format('-'*20))
	all_file_info.groupby('bytes')\
		.filter( lambda group: len(group) > 1 )\
		.sort_values(
			by=['bytes', 'min_time'],
			ascending=[True],
			inplace=True)\
		.loc[:,'f'] = p.Series(np.random.randn(sLength), index=df1.index)

	# iterate over groups
	for name, group in all_file_info.groupby('bytes'):
		print(name)
		print(type(group))
		print(group)

	print("{0} applymap to remaining elements {0}".format('-'*20))
	print(all_file_info.groupby('bytes')\
		.filter( lambda group: len(group) > 1 )\
		.applymap( lambda x: "{0} v".format(x) ))

	pandas.merge(left, right, how='inner', on=None, left_on=None, right_on=None,
		left_index=False, right_index=False, sort=False,
		suffixes=('_x', '_y'), copy=True, indicator=False)
	"""

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
