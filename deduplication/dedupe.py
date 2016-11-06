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


def main(args, logger):
	logger.info("Beginning walk at '{dir_tree_root}'".format(
		dir_tree_root=args.within_directory
	))
	for dirpath, dirnames, filenames in os.walk(
			args.within_directory, topdown=False, onerror=None):
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
	
