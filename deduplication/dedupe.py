#!/usr/bin/env python
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


import logging
import config
logger = logging.getLogger(config.APP_NAME)
import cli


def main(args):
	logger.debug("main")


if __name__ == '__main__':
	cli.run(main)	# only bootstrapping stuff in there, no app-specific code
