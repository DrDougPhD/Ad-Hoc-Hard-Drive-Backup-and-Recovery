#!/usr/bin/env python3

import os
import sys
from collections import defaultdict
from pprint import pprint


def count_file_types_within(directory_to_walk):
	file_type_counts = defaultdict(int)

	for dirpath, _, filenames in os.walk(directory_to_walk):
		for file in filenames:
			file_prefix, file_extension = os.path.splitext(file)
			file_type_counts[file_extension.lower()] += 1

	return sorted(
		[(ext, file_type_counts[ext]) for ext in file_type_counts],
		key=lambda t: t[1],
		reverse=True
	)


def write_counts_to_stdout(file_type_counts):
	for ext_count in file_type_counts:
		print("{0}:\t{1}".format(ext_count[0], ext_count[1]))


if __name__ == "__main__":
	directory_to_walk = sys.argv[-1]
	file_type_counts = count_file_types_within(directory_to_walk)
	write_counts_to_stdout(file_type_counts)

