import sys
import collections
import humanfriendly
import os

root_directory = sys.argv[-1]
file_type_counts = collections.defaultdict(int)
file_type_sizes = collections.defaultdict(int)

longest_extension_length = float('-inf')
for directory, subdirectory, files in os.walk(root_directory):
    print(directory, end='\r')
    for filename in files:
        file_path = os.path.join(directory, filename)
        prefix, ext = os.path.splitext(filename)
        size = os.path.getsize(file_path)
        
        file_type_counts[ext] += 1
        file_type_sizes[ext] += size

        longest_extension_length = max(longest_extension_length, len(ext))

most_frequent_file_type = float('-inf')
for count in file_type_counts.values():
    most_frequent_file_type = max(most_frequent_file_type, count)

longest_count_number = len(str(most_frequent_file_type))

for extension, occupied_size in file_type_sizes.items():
    count = file_type_counts[extension]    
    print('{0}  {1}  {2: >5}'.format(
        extension.ljust(longest_extension_length),
        str(count).center(longest_count_number),
        humanfriendly.format_size(occupied_size)
    ))
