#!/usr/bin/env python3
"""

TODO
	* Show average and standard deviation of file-sizes for each extension as
		a command-line graph
			e.g.
				filesizes:  1K  10K  100K  1M  10M  100M  1G  10G  100G  1T
				         +-------------------------------------------------------------
				    .mkv |               ----+++++#++++----
				    .avi |                     --++#++--
				   .flac |                 --++#++--
				         +-------------------------------------------------------------
	* Show total consumed space per file-size as a command-line graph
			e.g.
				 occupied:  1K  10K  100K  1M  10M  100M  1G  10G  100G  1T  10T
				         +-------------------------------------------------------------
				    .mkv |                                                 #     5.2 TB
				    .avi |                                            #         30.4 GB
				   .flac |                                    #                100.2 GB
				         +-------------------------------------------------------------

"""

import os
import sys
from collections import defaultdict
from pprint import pprint


def count_file_types_within(directory_to_walk):
	file_type_counts = defaultdict(int)

	for dirpath, _, filenames in os.walk(directory_to_walk):
		for file in filenames:
			file_prefix, file_extension = os.path.splitext(file)

			if file_extension == "":
				file_extension = "(none)"

			file_type_counts[file_extension.lower()] += 1

	return sorted(
		[(ext, file_type_counts[ext]) for ext in file_type_counts],
		key=lambda t: t[1],
		reverse=True
	)


def write_counts_to_stdout(file_type_counts):
	# iterate over file extensions and measure the widest one, for pretty
	# printing
	max_width_extension = max(
		file_type_counts,
		key=lambda c: len(c[0])
	)[0]
	max_width = len(max_width_extension)

	for ext_count in file_type_counts:
		print("{0}:\t{1}".format(ext_count[0].rjust(max_width), ext_count[1]))


if __name__ == "__main__":
	directory_to_walk = sys.argv[-1]
	file_type_counts = count_file_types_within(directory_to_walk)
	write_counts_to_stdout(file_type_counts)

