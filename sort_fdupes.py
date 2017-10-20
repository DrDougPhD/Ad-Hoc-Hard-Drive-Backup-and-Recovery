import os
import sys
import humanize
import linecache
import termcolor


def main(fdupes_log_path):
    fdupes_log = open(fdupes_log_path)
    duplicates = []
    line_index = 0
    for file_size_line in fdupes_log:
        duplicate_file_size = int(file_size_line.split(' ')[0])
        log_line_indices = []
        file_path_line = next(fdupes_log).strip()
        line_index += 1
        while file_path_line:
            log_line_indices.append(line_index)
            file_path_line = next(fdupes_log).strip()
            line_index += 1

        savings = duplicate_file_size*(len(log_line_indices)-1)
        duplicates.append((duplicate_file_size, savings, log_line_indices))
        line_index += 1

    print_sorted(duplicates, fdupes_log_path)


def print_sorted(duplicates, fdupes_log_path):
    print('='*120)
    duplicates.sort(key=lambda x: x[1])
    for size, savings, log_file_indices in duplicates:
        human_size = humanize.naturalsize(size, binary=True)
        human_savings = humanize.naturalsize(savings, binary=True)
        print('{} in savings - {} per file'.format(
            termcolor.colored(human_savings, 'red'),
            termcolor.colored(human_size, 'cyan')
        ))
        print('\n'.join([get_line(fdupes_log_path, i) 
                         for i in log_file_indices]))
        print('-'*120)


def get_line(file_path, line_number):
    return linecache.getline(file_path, line_number+1).strip()


if __name__ == '__main__':
    fdupes_log = sys.argv[-1]
    main(fdupes_log)

