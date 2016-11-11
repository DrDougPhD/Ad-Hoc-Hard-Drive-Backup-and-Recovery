import sys
import humanize
import os

SIZE_THRESHOLD = 1000*1000

def truncate_url(path, to_length=70):
	dirname, filename = os.path.split(path)
	filename_length = len(filename)
	path_parts = dirname.split('/')
	dirname += '/'
	
	while to_length <= len(dirname)+filename_length:
		path_parts = path_parts[1:]
		dirname = '.../' + '/'.join(path_parts) + '/'
	truncated_path = dirname + filename
	return truncated_path

with open(sys.argv[1]) as f:
	redundant_files = []
	for line in f:
		line = line.strip()
		print("---\t{}".format(line))
		if line:
			if line[0] != '/':
				new_group = {
					'files':[],
					'savings_if_deduped': 0,
					'file_size': int(line.split()[0])
				}
				redundant_files.append(new_group)
			else:
				files = new_group['files']
				if files:
					new_group['savings_if_deduped'] += new_group['file_size']
				files.append(line)

	redundant_files.sort(key=lambda group: group['savings_if_deduped'], reverse=True)
	large_enough_savings = lambda grp: grp['savings_if_deduped'] > SIZE_THRESHOLD

	# summarize the files that would be deleted, along with how much space
	# is reclaimed by deleting all files above that line
	running_total_savings = 0
	print('#'*80)
	print("# {path:^69}  {savings:^5} #".format(path="Files to delete (truncated paths)", savings="Size"))
	for duplicate_group in filter(large_enough_savings, redundant_files):
		files_to_delete = duplicate_group['files'][1:]
		for file in files_to_delete:
			running_total_savings += duplicate_group['file_size']
			print("# {path:>69}  {running_total_savings:>5} #".format(
				path=truncate_url(file, to_length=69),
				running_total_savings=humanize.naturalsize(
					running_total_savings,
					gnu=True
			)))
	print('#'*80)

	# create shell commands to perform deletion
	for duplicate_group in filter(large_enough_savings, redundant_files):
		original_file = duplicate_group['files'][0]
		print("#"*40 + " Original: '{}'".format(original_file))
		files_to_delete = duplicate_group['files'][1:]
		for file in files_to_delete:
			print("rm '{}'".format(file))
			print("ln -s '{original_file}' '{deleted_file_path}'".format(
				original_file=original_file,
				deleted_file_path=file,
			))

