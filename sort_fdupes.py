import os
import sys
import humanize

fdupes_log = open(sys.argv[-1])
duplicates = []
for line in fdupes_log:
    duplicate_file_size = int(line.split(' ')[0])
    files = []
    f = next(fdupes_log)
    while f:
        files.append(f)
    duplicates.append((duplicate_file_size, files))

duplicates.sort(key=lambda x: x[0])
for size, files in duplicates:
    human_size = humanize.naturalsize(size, binary=True)
    print(human_size)
    print('\n'.join(files))
    print('')

