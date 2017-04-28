#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SYNOPSIS

	python files_in_there_but_not_here.py [-h,--help] [-v,--verbose]


DESCRIPTION

	Given a target directory and a list of other directories, list the files
    that exist within the other directories but are absent within the target.


ARGUMENTS

	-h, --help	        show this help message and exit
	-v, --verbose       verbose output


AUTHOR

	Doug McGeehan <djmvfb@mst.edu>


LICENSE

	Copyright 2017  - GNU GPLv3


TODO

    Implement interprocess-communicating threading, where the walking of the
    target directory communicates with the walkers of the other directories.

"""

__appname__ = 'files_in_there_but_not_here'
__version__ = '0.0pre0'
__license__ = 'GNU GPLv3'
__indev__ = False


import argparse
from datetime import datetime
import sys
import os
import collections
import logging
logger = logging.getLogger(__name__)
from lib.lineheaderpadded import hr
import progressbar


def main(args):
    # Verify that the target directory is not listed twice
    if args.target == args.reference:
        logger.warning("It's not useful to have the target directory also"
                       " be in the other directories.")
        logger.warning('Execution is aborted.')
        sys.exit(1)

    # Walk the directories for their constituent files.
    relative_subdirectory_index = len(args.target)
    target_files = set()
    for subdirectory, directory_names, files in os.walk(args.target):
        relative_subdirectory = subdirectory[relative_subdirectory_index:]
        for filename in files:
            # Skip over symbolic links.
            if os.path.islink(os.path.join(subdirectory,
                                           filename)):
                continue

            target_files.add(os.path.join(relative_subdirectory, filename))

    reference_files = set()
    relative_subdirectory_index = len(args.reference)
    for subdirectory, directory_names, files in os.walk(args.reference):
        relative_subdirectory = subdirectory[relative_subdirectory_index:]
        for filename in files:
            # Skip over symbolic links.
            if os.path.islink(os.path.join(subdirectory,
                                           filename)):
                continue

            reference_files.add(os.path.join(relative_subdirectory,
                                             filename))

    missing_files = reference_files - target_files
    for file in missing_files:
        print(file)


def setup_logger(args):
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    # todo: place them in a log directory, or add the time to the log's
    # filename, or append to pre-existing log
    log_file = os.path.join('/tmp', '.log')
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()

    if args.verbose:
        ch.setLevel(logging.DEBUG)
    else:
        ch.setLevel(logging.INFO)

    # create formatter and add it to the handlers
    line_numbers_and_function_name = logging.Formatter(
        "%(levelname)s [%(filename)s:%(lineno)s - %(funcName)20s() ] "
        "%(message)s")
    fh.setFormatter(line_numbers_and_function_name)
    ch.setFormatter(line_numbers_and_function_name)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)


def get_arguments():
    parser = argparse.ArgumentParser(
        description="Description printed to command-line if -h is called."
    )
    # during development, I set default to False so I don't have to keep
    # calling this with -v
    parser.add_argument('-v', '--verbose', action='store_true',
                        default=__indev__,
                        help='Enable debugging messages (default: False)')
    parser.add_argument('target', metavar='TARGET_DIR',
                        help='The target directory that might not contain'
                             ' files in the other directories.')
    parser.add_argument('reference', metavar='REFERENCE_DIR',
                        help='The other directory that might'
                             ' contain files not in the target.')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    try:
        start_time = datetime.now()

        args = get_arguments()
        setup_logger(args)

        # figure out which argument key is the longest so that all the
        # parameters can be printed out nicely
        logger.debug('Command-line arguments:')
        length_of_longest_key = len(max(vars(args).keys(),
                                        key=lambda k: len(k)))
        for arg in vars(args):
            value = getattr(args, arg)
            logger.debug('\t{argument_key}:\t{value}'.format(
                argument_key=arg.rjust(length_of_longest_key, ' '),
                value=value))

        logger.debug(start_time)

        main(args)

        finish_time = datetime.now()
        logger.debug(finish_time)
        logger.debug('Execution time: {time}'.format(
            time=(finish_time - start_time)
        ))
        logger.debug("#" * 20 + " END EXECUTION " + "#" * 20)

        sys.exit(0)

    except KeyboardInterrupt as e:  # Ctrl-C
        raise e

    except SystemExit as e:  # sys.exit()
        raise e

    except Exception as e:
        logger.exception("Something happened and I don't know what to do D:")
        sys.exit(1)
