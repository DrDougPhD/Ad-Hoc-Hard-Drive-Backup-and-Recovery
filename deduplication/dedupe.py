#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
SYNOPSIS

	python <blah>.py [-h,--help] [-v,--verbose]


DESCRIPTION

	Iterate over files in a directory


ARGUMENTS

	-h, --help		show this help message and exit
	-v, --verbose		verbose output


AUTHOR

	Doug McGeehan <doug.mcgeehan@mst.edu>


LICENSE

	Copyright 2016 Doug McGeehan. All rights reserved.

"""

__version__ = "0.0pre0"


from datetime import datetime
import logging
import config
import cli
import os
import sys


def process_files(dirpath, dirnames, filenames):
	"""
	Process each of the filenames.
	Obtain their filesize, timestamps.
	Add their filesizes into a dictionary associating bytesizes to
	absolute file paths.
	If one file was previously found with the bytesize as one of these
	files, then compute the checksum for the previous file.
		Append this file to the list.
		Maybe that should trigger some checksum function automatically
		if it sees the list now has more than 1 file?
	Checksum creation is added to a dictionary associating checksums with
	absolute file paths.
	Each directory is augmented with the summed filesize of all files
	stored within.
		Also possibly the oldest file timestamp and newest file
		timestamp.
	"""
	pass


def main(args, logger):
	root_directory = str(args.within_directory.resolve())
	logger.info("Beginning walk at '{root_directory}'".format(
		root_directory=root_directory
	))
	for dirpath, dirnames, filenames in os.walk(root_directory,
			topdown=False, onerror=None):
		logger.debug('\t{dirpath}'.format(dirpath=dirpath))


if __name__ == '__main__':
	"""
	Main driver for code
	"""
	start_time = datetime.now()

	args = cli.get_arguments()
	logger = cli.setup_logger(args)
	logger.info(args)
	logger.debug(start_time)

	try:
		main(args, logger)

	except KeyboardInterrupt as e: # Ctrl-C
		raise e

	except SystemExit as e: # sys.exit()
		raise e

	except Exception as e:
		logger.exception("Something happened and I don't know what to do D:")
		sys.exit(1)

	finally:
		finish_time = datetime.now()
		logger.debug(finish_time)
		logger.debug('Execution time: {time}'.format(
			time=(finish_time - start_time)
		))
		logger.debug("#"*20 + " END EXECUTION " + "#"*20)

		sys.exit(0)
	
