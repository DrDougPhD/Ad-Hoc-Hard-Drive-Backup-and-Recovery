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

"""

__appname__ = 'files_in_there_but_not_here'
__version__ = '0.0pre0'
__license__ = 'GNU GPLv3'


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
    if args.target in args.others:
        logger.warning("It's not useful to have the target directory also"
                       " be in the other directories.")
        logger.warning('Execution is aborted.')
        sys.exit(1)

    # Build a list of files in each of the supplied directories
    logger.info(hr('Directory walking'))
    logger.info('Walking target directory')
    files_in_target = list_files(within=args.target)

    file_count_in_target = file_count_in(directory_listing=files_in_target)
    logger.info('{0: >8} files found within target'.format(
        file_count_in_target))

    logger.info(hr('Walking other directories', '-'))
    files_in_others = collections.defaultdict(set)
    for other_dir in args.others:
        logger.info(other_dir)
        found_files = list_files(within=other_dir)
        for filesize, files in found_files.items():
            files_in_others[filesize].update(files)

    file_count_in_others = file_count_in(directory_listing=files_in_others)
    logger.info('{0: >8} files found within other directories'.format(
        file_count_in_others))

    logger.info(hr('Comparing the files in others to those in target'))

    absent_files = []
    filesize_cluster_count = len(files_in_others)
    with progressbar.ProgressBar(max_value=filesize_cluster_count) as progress:
        for i, (filesize, files) in enumerate(files_in_others.items()):

            # If there were no files found within the target directory that
            # have the given file size, then record all of the files of that
            # filesize that exist within the other directories.
            if filesize not in files_in_target:
                absent_files.extend(files)

            progress.update(i)

    # Print out the missing files.
    logger.info(hr('Complete'))
    logger.info('{} files were found in the other directories but absent from'
                ' the target directory'.format(len(absent_files)))
    for other_directory, relative_file_path in absent_files:
        print(os.path.join(other_directory, relative_file_path))

    # Create the copy/move script if the user specified one.
    if args.script_type is not None:
        script_maker = globals()[args.script_type]
        script_lines = script_maker(missing_files=absent_files,
                                    target_directory=args.target)
        print('\n'.join(script_lines))


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Script generators
#
def cp(missing_files, target_directory):
    script_lines = []
    make_directory_template = 'mkdir --parents "{}"'
    copy_command_template = 'cp -v "{source}" "{destination}"'

    target_directory = os.path.abspath(target_directory)

    for directory, relative_file_path in missing_files:

        # add a line to create the directory path in the target directory
        relative_directory_path = os.path.dirname(relative_file_path)
        script_lines.append(make_directory_template.format(
            relative_directory_path))

        # add a command to perform the copying
        source_directory_abs = os.path.abspath(directory)
        script_lines.append(copy_command_template.format(
            source=os.path.join(source_directory_abs, relative_file_path),
            destination=os.path.join(target_directory, relative_file_path)))

    return script_lines


def rsync():
    raise NotImplementedError('Rsync script creation is not yet created')


def scp():
    raise NotImplementedError('scp script creation is not yet created')


def mv():
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def file_count_in(directory_listing):
    return sum(map(
        lambda filesize: len(directory_listing[filesize]),
        directory_listing.keys()))


def list_files(within):
    if within[-1] != '/':
        within = within + '/'

    # Clip the file paths returned through walking to only include the path
    # of a file relative to the "within" directory root.
    remove_path_before = len(within)
    found_files = collections.defaultdict(set)
    for subdirectory, directory_names, filenames in os.walk(within):
        relative_subdirectory = subdirectory[remove_path_before:]

        for f in filenames:
            full_filepath = os.path.join(subdirectory, f)
            file_size = os.path.getsize(full_filepath)

            relative_filepath = os.path.join(relative_subdirectory, f)
            found_files[file_size].add((within, relative_filepath))

    return found_files


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
    parser.add_argument('-o', '--output-file', dest='output_filepath',
                        type=os.path.abspath, default=None,
                        help='The output file to write the paths of the'
                             ' absent files (default: write to stdout).')
    parser.add_argument('-a', '--as-absolute-paths',
                        dest='format_paths_to_absolute', action='store_true',
                        default=False,
                        help='Output file paths should be absolute paths'
                             ' (default: False - relative paths)')
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='Enable debugging messages (default: False)')
    parser.add_argument('-s', '--create-copy-script', dest='script_type',
                        choices=['cp', 'rsync', 'scp', 'mv'],
                        default=None,
                        help='Create a script that can be executed to'
                             ' copy/move the missing files from the source'
                             ' into the target (default: no script)')
    parser.add_argument('target', metavar='TARGET_DIR',
                        help='The target directory that might not contain'
                             ' files in the other directories.')
    parser.add_argument('others', metavar='OTHER_DIR',
                        nargs='+', help='The other directories that might'
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
