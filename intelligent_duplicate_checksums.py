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
  Logging.
  Checksum from Python library.
  Duplicates with highest space occupancy should be closer to the top.
  Within duplicate groups, sort by timestamp in descending order.
  No dependency on previously-created file; walk directory instead, building
    list of potential duplicates along the way and calculating hashes as
    needed.
  Given a files containing urls and file sizes, only compute the md5sums
    of those files with matching sizes.
  Given two files containing urls and files sizes, only compute the md5sums
    of those files with matching sizes.
  Command-line input: --min-file-size specifies a lower bound on filesizes,
    above which a file will have its md5hash checked. Intuition is that small
    files are more likely to be the same, especially if two operating systems
    are backed up in the same hard drive (very similar files within each).
  Command-line input: --dry-run?
"""

import sys
import pandas
import numpy
import subprocess
from collections import defaultdict
import os
import hurry.filesize


"""
Calculate a checksum for the specified file
"""
checksum = lambda path: subprocess.check_output(
		['md5sum', path],
		universal_newlines=True
	).split()[0]


if __name__ == "__main__":
	"""
	The input to this script is a list of file paths and file sizes.
	Assume the first column is the path of a file, and the second column is the
	file's size in bytes. Columns are separated by tabs. All other columns are
	ignored.
	"""
	infile = sys.argv[1]
	all_file_info = pandas.read_table(
		filepath_or_buffer=infile,
		names=['url', 'bytes', 'atime', 'ctime', 'mtime'],
		usecols=['url', 'bytes'],
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

	# Only keep files that have filesizes equal to other files (potential
	# duplicates)
	same_sized_files = all_file_info.groupby('bytes')\
		.filter(lambda group: len(group) > 1)

	# Associate checksums with list of files
	duplicates = defaultdict(list)
	print("{0} begin md5sum format {0}".format('-'*20))
	for i, row in same_sized_files.iterrows():
		try:
			x = checksum(row.url)
		except:
			print("Error: file not found, skipping '{0}'".format(
				row.url
			), file=sys.stderr)
		else:
			print("{0}  {1}".format(x, row.url))
			duplicates[x].append(row)

	print("{0} end md5sum format {0}".format('-'*20))

	# Prepare to write results out to a file
	outfile_url = os.path.join(
		os.path.dirname(infile),
		"duplicates.{0}".format(os.path.basename(infile))
	)
	# Calculate how much space would be saved if all duplicates were
	# removed
	space_savings = 0
	with open(outfile_url, 'w') as outfile:
		# Order the checksums by how many duplicate files exist with
		# the checksum
		for x in sorted(duplicates, key=lambda x: len(duplicates[x]),
				reverse=True):
			files_with_checksum = duplicates[x]
			n = len(files_with_checksum)-1
			group_space_savings = n * files_with_checksum[0].bytes
			space_savings += group_space_savings

			for r in files_with_checksum:
				humanized_bytesize = hurry.filesize.size(
					r.bytes,
					system=hurry.filesize.si
				)
				outfile.write("{0}\t{1}\t{2}\t{3}\n".format(
					x, humanized_bytesize, r.url, r.bytes
				))

	print("Processing complete.")
	print("Checksum files written to {0}".format(outfile_url))
	print("Deduplication will save {0}.".format(
		hurry.filesize.size(space_savings, system=hurry.filesize.si)
	))
