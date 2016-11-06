#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Command-line interface for application.
"""

import config
import argparse
import utils
import os
from pathlib import Path
import logging


def get_arguments():
	parser = argparse.ArgumentParser(
		description=("Intelligently calculate checksums on only those "
			"files which may have duplicates in another location "
			"under the searched directory tree.")
	)
	parser.add_argument('-v', '--verbose', action='store_true',
		default=True, help='verbose output')
	parser.add_argument('-d', '--directory',
		dest='within_directory',
		default='.', type=Path,
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
	parser.add_argument('-l', '--log-directory',
		dest='log_directory',
		default='logs', type=Path,
		help='path into which logs are saved',
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
