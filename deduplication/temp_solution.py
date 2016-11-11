import sys
from pprint import pprint

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
	pprint(redundant_files)
