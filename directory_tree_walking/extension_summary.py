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
from lib.lineheaderpadded import hr

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
import hurry.filesize as filesize

logger = logging.getLogger(__name__)


def main(args):
    summary = DirectorySummary(root=args.target)
    summary.walk()
    summary.print()
    summary.plot()


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
                self.walk_path_to_root(extension, file_size, parent_directory)

    def walk_path_to_root(self, extension, file_size, parent_directory):
        while parent_directory != self.root:
            directory_summary = self.directory_based_file_types[
                parent_directory]

            if extension not in directory_summary:
                directory_summary[extension] = []

            directory_summary[extension].append(file_size)

            parent_directory = os.path.dirname(parent_directory)

    def print(self):
        cli_plot = CommandLineHorizontalPlot(data=self.file_type_sizes)
        cli_plot.plot(
            title='Space Allocation per Extension: {}'.format(self.root),
            max_value=self.total_size,
            aggregate_fn=sum,
            value_fmt_fn=lambda x: filesize.size(x, system=filesize.si)
                                           .rjust(4))
        cli_plot.plot(
            title='File Counts per Extension: {}'.format(self.root),
            max_value= self.num_files,
            aggregate_fn=len)


    def plot(self):
        # partition directories by their dominating extension
        dominating_extensions = {k: [] for k in self.file_type_sizes.keys()}
        for directory_path, extension_stats in \
                self.directory_based_file_types.items():

            stats = DirectoryExtensionStats(path=directory_path,
                                            extension_stats=extension_stats)
            dominating_extensions[stats.dominating_ext].append(stats)

        logger.debug(hr('Dominating Extentions'))
        for extension in list(dominating_extensions.keys()):
            ext_stats = dominating_extensions[extension]
            if not ext_stats:
                del dominating_extensions[extension]
                continue

            ext_stats.sort(
                key=lambda stats: stats.proportion_files_with_dominating_ext,
                reverse=True)

            logger.debug(hr(extension, '-'))
            for stats in ext_stats:
                stats.sort_extensions()
                stats.summary()

        # Print out summary of the walked directories
        logger.debug(hr('Summary'))

        num_unique_extensions = len(self.file_type_sizes)
        logger.debug('Number of unique extension: {}'.format(
            num_unique_extensions))

        num_subdirectories = len(self.directory_based_file_types)
        logger.debug('{0} subdirectories contained within {1}'.format(
            num_subdirectories, self.root
        ))

        max_length_of_leaf_directory_path = len(
            max(self.directory_based_file_types.keys(),
                key=len))
        logger.debug('Max length of directory path: {} chars'.format(
            max_length_of_leaf_directory_path))


        # ordered_directories = collections.OrderedDict()
        # for extension, path_stats in dominating_extensions.items():
        #     sorted_directories_by_max_portion = []
        #     for directory_path, ext_stats_in_dir in path_stats.items():
        #         sorted_directories_by_max_portion.append((
        #             directory_path, ext_stats_in_dir[extension]
        #         ))
        #     #sorted_directories_by_max_portion.sort(key=lambda)
        plot = DirectoryBreakdownFigure(
            extension_stats=dominating_extensions,
            margin_width=max_length_of_leaf_directory_path,
            plot_height=num_subdirectories,
        )
        plot.plot(save_to='extension_breakdown.pdf')


import matplotlib.pyplot as plt
import numpy
import itertools
color_wheel = itertools.cycle(['blue', 'green', 'red'])
class DirectoryBreakdownFigure(object):
    bar_colors = {}

    def __init__(self, extension_stats, margin_width, plot_height):
        self.extension_stats = extension_stats
        self.margin_width = margin_width
        self.plot_height = plot_height

    def plot(self, save_to):
        verticle_space = int(self.plot_height/6)
        horizontal_space = int(self.margin_width/10) + 3

        logger.debug('Verticle space:   {}'.format(verticle_space))
        logger.debug('Horizontal space: {}'.format(horizontal_space))

        figure, axes = plt.subplots(
            figsize=(horizontal_space, verticle_space))

        # create the bar for each directory
        directory_labels = []
        y_val = 0
        right_y_axis = axes.twinx()
        for ext, dominated_ext_stats in self.extension_stats.items():

            for directory_stats in dominated_ext_stats:
                directory_labels.append(directory_stats.path)

                bar_widths, bar_offsets, colors = self.single_barh(
                    ext_stats=directory_stats)

                # every horizontal bar created for this directory will be
                #  located on the same y height
                num_bars = len(bar_widths)
                y_vals = numpy.zeros(num_bars) + y_val + .5
                right_y_axis.barh(bottom=y_vals,
                          width=bar_widths,
                          height=1.05,
                          left=bar_offsets,
                          color=colors,
                          linewidth=0)
                          #edgecolor='black')

                y_val += 1

        logger.debug('{} bars produced'.format(y_val))
        logger.debug('{} directories considered'.format(self.plot_height))

        # add directories to the right of the plot
        y_ticks = numpy.arange(len(directory_labels))+0.5
        right_y_axis.set_yticks(y_ticks)
        right_y_axis.set_yticklabels(directory_labels)
        right_y_axis.tick_params(axis='y', which='both', length=0)
        right_y_axis.invert_yaxis()
        axes.set_xlim([0, 1])
        axes.set_ylim([0, self.plot_height])
        right_y_axis.set_ylim([0, self.plot_height])
        axes.invert_xaxis()

        # hide the tickmarks on the left y-axis
        axes.set_yticks([])
        axes.set_xticks([])
        plt.tight_layout()
        plt.savefig(save_to)

    def single_barh(self, ext_stats):
        bar_widths = []
        bar_offsets_from_left = [0]
        colors = []
        for ext, proportion in ext_stats:
            if ext not in DirectoryBreakdownFigure.bar_colors:
                DirectoryBreakdownFigure.bar_colors[ext] = next(color_wheel)

            colors.append(DirectoryBreakdownFigure.bar_colors[ext])
            bar_widths.append(proportion+.05)

            # set the offet for the bar to be drawn after this one
            bar_offsets_from_left.append(proportion+bar_offsets_from_left[-1])

        # remove the last offset, as it doesn't correspond to any extension
        # due to the manner in which the bar offsets are created
        bar_offsets_from_left.pop()

        return bar_widths, bar_offsets_from_left, colors



class DirectoryExtensionStats(object):
    def __init__(self, path, extension_stats):
        self.path = path
        self.extension_stats = extension_stats

        ext, count, space, proportional_count = self._determine_dominating_ext(
            extension_stats)
        self.dominating_ext = ext
        self.num_files_with_dominating_ext = count
        self.space_allocated_to_dominating_ext = space
        self.proportion_files_with_dominating_ext = proportional_count

    def _determine_dominating_ext(self, extension_stats):
        # determine the extension that dominates this path
        ext = max(extension_stats.keys(),
                  key=lambda k: len(extension_stats[k]))
        count = len(extension_stats[ext])
        space = sum(extension_stats[ext])

        # count the total number of files within this directory
        ext_count_pairs = map(lambda k: (k, len(extension_stats[k])),
                              extension_stats.keys())
        self.num_files_within_dir = sum(map(lambda v: v[1],
                                       ext_count_pairs))
        # record the proportion of files within this directory that have the
        # dominating extension
        proportion = count / self.num_files_within_dir
        return ext, count, space, proportion

    def summary(self):
        logger.debug(self.path)
        # logger.debug('Dominated by: {0: >7} - {1: >6}, {2: >4}'.format(
        #         self.dominating_ext,
        #         '{:.1%}'.format(self.proportion_files_with_dominating_ext),
        #         filesize.size(self.space_allocated_to_dominating_ext,
        #                       system=filesize.si)
        #     ))

        logger.debug('┌─────────┬─────────┬────────┐')
        for ext, portion in self.sorted_extensions.items():
            logger.debug('│ {0: ^7} │ {1: ^7} │  {2: >4}  │'.format(
                ext,
                '{:.1%}'.format(portion),
                filesize.size(sum(self.extension_stats[ext]),
                              system=filesize.si)
            ))
        logger.debug('└─────────┴─────────┴────────┘')

    def sort_extensions(self):
        ext_portion_pair = map(lambda x: (x, len(self.extension_stats[x])),
                               self.extension_stats.keys())
        ext_portion_pair = sorted(ext_portion_pair,
                                  key=lambda x: x[1],
                                  reverse=True)
        sorted_extensions = collections.OrderedDict()
        for ext, portion in ext_portion_pair:
            sorted_extensions[ext] = portion/self.num_files_within_dir

            self.sorted_extensions = sorted_extensions

    def __iter__(self):
        for extension, proportion in self.sorted_extensions.items():
            yield (extension, proportion)

class CommandLineHorizontalPlot(object):
    def __init__(self, data):
        self.data = data
        self.max_key_length = len(max(data.keys(), key=len))

    def plot(self, max_value, title, aggregate_fn, value_fmt_fn=None):
        if value_fmt_fn is None:
            value_fmt_fn = lambda x: x

        title = self.generate_title(title)
        top_border = self.generate_horizontal_border(corner='┌')
        plot_lines = self.generate_internal_plotlines(data=self.data,
                                                      max_value=max_value,
                                                      aggregate_fn=aggregate_fn,
                                                      value_fmt_fn=value_fmt_fn)
        bottom_border = self.generate_horizontal_border(corner='└')

        plot_content = '\n'.join([
            title,
            top_border,
            *plot_lines,
            bottom_border,
        ]) + '\n'
        print(plot_content)


    def generate_title(self, title):
        title = '{margin}   {title}'.format(
            margin=self.margin(),
            title=title,
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

    def generate_internal_plotlines(self, data, max_value, aggregate_fn,
                                    value_fmt_fn):
        lines = []

        sorted_and_aggregated_data = sorted(
            [(k, aggregate_fn(data[k])) for k in data],
            key=lambda x: x[1],
            reverse=True
        )
        for key, value in sorted_and_aggregated_data:
            percentage = value / max_value
            percentage_string = '{:.1%}'.format(percentage)\
                                        .rjust(5)
            formatted_value = value_fmt_fn(value)

            lines.append('{margin} │{bar}│'
                         ' {percentage}, {value}'.format(
                margin=self.margin(key=key),
                bar=self.internal_data_line(percentage=percentage),
                percentage=percentage_string,
                value=formatted_value,
            ))

        return lines

    def internal_data_line(self, percentage, width=100, char='+'):
        data_chars = '+' * int(width*percentage)
        padded_data_line = data_chars.ljust(width)
        return padded_data_line



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
