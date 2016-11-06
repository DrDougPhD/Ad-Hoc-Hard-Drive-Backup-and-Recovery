#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Command-line interface for application.
"""

from datetime import datetime
import sys
import config
import argparse
import utils
import os

import logging
logger = utils.get_descendant_logger(__name__)


def run(driver):
	"""
	Main driver for code
	"""
	try:
		start_time = datetime.now()

		args = get_arguments()
		setup_logger(args)
		logger.debug(start_time)

		driver(args)

		finish_time = datetime.now()
		logger.debug(finish_time)
		logger.debug('Execution time: {time}'.format(
			time=(finish_time - start_time)
		))
		logger.debug("#"*20 + " END EXECUTION " + "#"*20)

		sys.exit(0)

	except KeyboardInterrupt as e: # Ctrl-C
		raise e

	except SystemExit as e: # sys.exit()
		raise e

	except Exception as e:
		logger.exception("Something happened and I don't know what to do D:")
		sys.exit(1)


def get_arguments():
	parser = argparse.ArgumentParser(
		description=("Intelligently calculate checksums on only those "
			"files which may have duplicates in another location "
			"under the searched directory tree.")
	)
	parser.add_argument('-v', '--verbose', action='store_true',
		default=True, help='verbose output')
	parser.add_argument('-d', '--directory',
		dest='root_directory',
		help='path to directory in which to search for dupes',
	)
	parser.add_argument('-m', '--min-filesize-checksum',
		dest='lowerbound_filesize',
		help='files smaller than this size will not be hashed',
		default=0
	)
	parser.add_argument('--dry-run',
		dest='is_dry_run', action='store_true',
		default=False,
		help="don't compute checksums, just walk directory"
	)

	return parser.parse_args()


def setup_logger(args):
	logger.setLevel(logging.DEBUG)

	# create file handler which logs even debug messages
	utils.create_directory_safely(config.LOG_DIR)
	fh = logging.FileHandler(
		os.path.join(config.LOG_DIR, config.APP_NAME + ".log")
	)
	fh.setLevel(logging.DEBUG)
	# create console handler with a higher log level
	ch = logging.StreamHandler()

	if args.verbose:
		ch.setLevel(logging.DEBUG)
	else:
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


