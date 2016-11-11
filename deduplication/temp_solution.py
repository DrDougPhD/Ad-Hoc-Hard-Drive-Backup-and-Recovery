import sys
import humanize
import os

SIZE_THRESHOLD = 1000*1000

def truncate_url(path, to_length=70):
	filename = os.path.basename(path)
	filename_length = len(filename)
	dirname = os.path.dirname(path)
	truncated_dirname = dirname + '/'
	while to_length <= len(truncated_dirname)+filename_length:
		dirname = os.path.dirname(dirname)
		truncated_dirname = dirname + '/.../'
	truncated_path = truncated_dirname + filename
	print('{path}\t{n} chars long'.format(
		path=truncated_path,
		n=len(truncated_path)
	))
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
	running_total_savings = 0
	for duplicate_group in filter(large_enough_savings, redundant_files):
		files_to_delete = duplicate_group['files'][1:]
		for file in files_to_delete:
			running_total_savings += duplicate_group['file_size']
			print(humanize.naturalsize(
				running_total_savings,
				gnu=True
			))
			print("{path}\t{running_total_savings:<5}".format(
				path=truncate_url(file, to_length=70),
				running_total_savings=humanize.naturalsize(
					running_total_savings,
					gnu=True
			)))
