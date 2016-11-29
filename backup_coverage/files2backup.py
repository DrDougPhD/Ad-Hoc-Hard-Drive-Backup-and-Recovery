#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Command-line interface for application.
"""

import argparse
import os
import logging
from collections import defaultdict


def main():
	args = get_arguments()
	primary_checksums, primary_files = load_checksum_file(args.primary_drive)
	backup_checksums, backed_up_files = load_checksum_file(args.backup_drive)
	vulnerable_files_checksums = primary_checksums - backup_checksums
	for h in vulnerable_files_checksums:
		print(primary_files[h][0])
	
	k = len(vulnerable_files_checksums)
	n = len(primary_checksums)
	print("{0} out of {1} files ({2}%) need backup!".format(
		k, n, (k*100.0)/n
	))

def load_checksum_file(checksum_file_path):
	checksums = set()
	filepaths_keyed_on_checksums = defaultdict(list)
	with open(checksum_file_path) as checksums_from_file:
		for file in checksums_from_file:
			broken_up_line = file.split()
			checksum = broken_up_line[0]
			file_path = " ".join(broken_up_line[1:])
			checksums.add(checksum)
			filepaths_keyed_on_checksums[checksum].append(file_path)
			#assert os.path.exists(file_path), "file doesn't exist: '{0}'".format(file_path)

	return checksums, filepaths_keyed_on_checksums


def get_arguments():
	parser = argparse.ArgumentParser(
		description=("Determine which files in the primary datastore "
			"are not backed up on the backup datastores.")
	)
	parser.add_argument('-v', '--verbose', action='store_true',
		default=False, help='verbose output')
	parser.add_argument('-p', '--primary-drive',
		dest='primary_drive',
		help='checksum file for files on the primary drive',
	)
	parser.add_argument('-b', '--backup-drive',
		dest='backup_drive',
		help='checksum file for files on the backup drive',
	)
	return parser.parse_args()


def setup_logger(args):
	logger = logging.getLogger(config.APP_NAME)
	logger.setLevel(logging.DEBUG)

	# create file handler which logs even debug messages
	args.log_directory.mkdir(exist_ok=True)
	fh = logging.FileHandler(str(
		args.log_directory / (config.APP_NAME + '.log')
	))

	# create console handler with a higher log level
	ch = logging.StreamHandler()

	if args.verbose:
		fh.setLevel(logging.DEBUG)
		ch.setLevel(logging.DEBUG)
	else:
		fh.setLevel(logging.INFO)
		ch.setLevel(logging.INFO)

	# create formatter and add it to the handlers
	fh.setFormatter(logging.Formatter(
		'%(asctime)s - %(name)s - %(levelname)s - %(message)s'
	))
	ch.setFormatter(logging.Formatter(
		'%(levelname)s - %(message)s'
	))
	# add the handlers to the logger
	logger.addHandler(fh)
	logger.addHandler(ch)

	return logger

if __name__ == "__main__":
	main()
