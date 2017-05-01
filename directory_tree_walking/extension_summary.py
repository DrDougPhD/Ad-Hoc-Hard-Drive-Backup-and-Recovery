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
__indev__ = True

import argparse
from datetime import datetime
import sys
import os
import collections
import logging
from hurry.filesize import size
from hurry.filesize import si

logger = logging.getLogger(__name__)


def main(args):
    summary = DirectorySummary(root=args.target)
    summary.walk()
    summary.print()

class DirectorySummary(object):
    def __init__(self, root):
        # Assert existence of the directory and return its absolute path
        self.root = self._existing_directory(root)

        self.file_type_sizes = collections.defaultdict(list)
        self.directory_based_file_types = collections.defaultdict(dict)

        self.total_size = 0
        self.num_files = 0

    def _existing_directory(self, directory):
        """
        Assert directory exists. If it does, return the absolute path of the 
        directory without the appended forward slash "/"
        :return: Absolute path to the provided directory.
        """
        assert os.path.isdir(directory), '"{}" is not a directory.'.format(
                                             directory)

        # If the directory ends with a forward slash, remove it
        if directory[-1] == '/':
            directory = os.path.dirname(directory)

        return os.path.abspath(directory)

    def walk(self):
        for subdirectory, directory_names, files in os.walk(self.root):
            self.num_files += len(files)

            for filename in files:
                file_path = os.path.join(subdirectory, filename)

                # Skip over symbolic links.
                if os.path.islink(file_path):
                    continue

                file_size = os.path.getsize(file_path)
                self.total_size += file_size
                filename_prefix, extension = os.path.splitext(filename)
                self.file_type_sizes[extension].append(file_size)

                parent_directory = os.path.dirname(file_path)
                while parent_directory != self.root:
                    directory_summary = self.directory_based_file_types[
                        parent_directory]

                    if extension not in directory_summary:
                        directory_summary[extension] = []

                    directory_summary[extension].append(file_size)

                    parent_directory = os.path.dirname(parent_directory)

    def print(self):
        cli_plot = CommandLineHorizontalPlot(
            title='Space Allocation per Extension: {}'.format(self.root),
            keys=self.file_type_sizes.keys(),
        )
        cli_plot.plot(data=self.file_type_sizes, max_value=self.total_size)

        # max_extension_length = len(max(self.file_type_sizes.keys(), key=len))
        #
        # # Print summed sizes
        # print('{space}  Space Allocation per Extension: {directory}'.format(
        #     space=' ' * (max_extension_length + 1),
        #     directory=self.root,
        # ))
        # print('{space}┌{border}┤'.format(
        #     space=' ' * (max_extension_length + 1),
        #     border='─' * 100,
        # ))
        # sorted_file_sizes = sorted(
        #     [(k, sum(self.file_type_sizes[k])) for k in self.file_type_sizes],
        #     key=lambda x: x[1],
        #     reverse=True
        # )
        # for extension, summed_size_for_extension in sorted_file_sizes:
        #     summed_size_pretty_print = size(summed_size_for_extension,
        #                                     system=si)
        #     summed_size_percentage = summed_size_for_extension/self.total_size
        #
        #     print('{extension} │ {bar}   ({percentage:.1%}, {filesize})'.format(
        #         extension=extension.rjust(max_extension_length, ' '),
        #         bar='+' * int(100 * summed_size_percentage),
        #         percentage=summed_size_percentage,
        #         filesize=summed_size_pretty_print,
        #     ))
        #
        # print('{space}└{border}┤\n'.format(
        #     space=' ' * (max_extension_length + 1),
        #     border='─' * 100,
        # ))
        #
        # # Print file numbers
        # print('{space}  File Counts per Extension in {directory}'.format(
        #     space=' ' * (max_extension_length + 1),
        #     directory=self.root,
        # ))
        # print('{space}┌{border}┤'.format(
        #     space=' ' * (max_extension_length + 1),
        #     border='─' * 100,
        # ))
        # sorted_file_sizes = sorted(
        #     [(k, len(self.file_type_sizes[k])) for k in self.file_type_sizes],
        #     key=lambda x: x[1],
        #     reverse=True
        # )
        # for extension, num_files_per_type in sorted_file_sizes:
        #     summed_size_percentage = num_files_per_type / self.num_files
        #
        #     print(
        #         '{extension} │ {bar}   ({percentage:.1%}, {file_count} files)'.format(
        #             extension=extension.rjust(max_extension_length, ' '),
        #             bar='+' * int(100 * summed_size_percentage),
        #             percentage=summed_size_percentage,
        #             file_count=num_files_per_type,
        #         ))
        #
        # print('{space}└{border}┤\n'.format(
        #     space=' ' * (max_extension_length + 1),
        #     border='─' * 100,
        # ))

    def plot(self):
        pass


class CommandLineHorizontalPlot(object):
    def __init__(self, title, keys):
        self.title = title
        self.axis_keys = keys
        self.max_key_length = len(max(keys, key=len))

    def plot(self, data, max_value):
        title = self.generate_title()
        top_border = self.generate_horizontal_border(corner='┌')
        plot_lines = self.generate_internal_plotlines(data=data,
                                                      max_value=max_value)
        bottom_border = self.generate_horizontal_border(corner='└')

        plot_content = '\n'.join([
            title,
            top_border,
            *plot_lines,
            bottom_border,
        ]) + '\n'
        print(plot_content)


    def generate_title(self):
        title = '{margin}   {title}'.format(
            margin=self.margin(),
            title=self.title,
        )
        return title

    def margin(self, key=None):
        if key is None:
            key = ' '

        return key.rjust(self.max_key_length)

    def generate_horizontal_border(self, corner):
        border = '{margin} {corner}{border}┤'.format(
            margin=self.margin(),
            corner=corner,
            border='─' * 100,
        )
        return border

    def generate_internal_plotlines(self, data, max_value):
        lines = []

        sorted_file_sizes = sorted(
            [(k, sum(data[k])) for k in data],
            key=lambda x: x[1],
            reverse=True
        )
        for extension, summed_size_for_extension in sorted_file_sizes:
            summed_size_pretty_print = size(summed_size_for_extension,
                                            system=si)
            summed_size_percentage = summed_size_for_extension / max_value

            lines.append('{margin} │ {bar}'
                         '   ({percentage:.1%}, {filesize})'.format(
                margin=self.margin(key=extension),
                bar='+' * int(100 * summed_size_percentage),
                percentage=summed_size_percentage,
                filesize=summed_size_pretty_print,
            ))

        return lines


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
                        help='The target directory to search')

    args = parser.parse_args()
    return args


def log_args(args):
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


if __name__ == '__main__':
    try:
        start_time = datetime.now()

        args = get_arguments()
        setup_logger(args)
        log_args(args)

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
