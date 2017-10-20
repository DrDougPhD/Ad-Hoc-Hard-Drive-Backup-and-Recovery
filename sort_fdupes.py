import os
import sys
import humanize
import linecache
import termcolor

minimum_file_savings = 1000000000

def main(fdupes_log_path):
    fdupes_log = open(fdupes_log_path, 'rb')
    duplicates = []
    line_index = 0
    for file_size_line in fdupes_log:
        duplicate_file_size = int(file_size_line.decode('utf-8').split(' ')[0])
        log_line_indices = []
        file_path_line = next(fdupes_log)
        line_index += 1
        while len(file_path_line) != 1:
            log_line_indices.append(line_index)
            file_path_line = next(fdupes_log)
            line_index += 1

        savings = duplicate_file_size*(len(log_line_indices)-1)
        if savings >= minimum_file_savings:
            duplicates.append((duplicate_file_size, savings, log_line_indices))
        line_index += 1

    print_sorted(duplicates, fdupes_log_path)


def print_sorted(duplicates, fdupes_log_path):
    print('='*120)
    with open(fdupes_log_path, 'rb') as f:
        fdupes_log_lines = f.readlines()

    duplicates.sort(key=lambda x: x[1], reverse=True)
    for size, savings, log_file_indices in duplicates:
        human_size = humanize.naturalsize(size, binary=True)
        human_savings = humanize.naturalsize(savings, binary=True)
        print('{} in savings - {} per file'.format(
            termcolor.colored(human_savings, 'red'),
            termcolor.colored(human_size, 'cyan')
        ))
        for index in log_file_indices:
            file_line = fdupes_log_lines[index][:-1]

            #file_line = get_line(fdupes_log_path, index)
            try:
                print(file_line.decode('utf-8'))
            except UnicodeDecodeError:
                print(file_line)

        print('-'*120)


def get_line(file_path, line_number):
    with open(file_path, 'rb') as f:
        for i, line in enumerate(f):
            if i == line_number:
                return line[:-1]


if __name__ == '__main__':
    fdupes_log = sys.argv[-1]
    main(fdupes_log)

