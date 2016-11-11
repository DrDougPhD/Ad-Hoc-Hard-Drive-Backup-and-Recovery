import sys
from pprint import pprint

with open(sys.argv[1]) as f:
	new_group = {'files':[]}
	redundant_files = [new_group]
	for line in f:
		line = line.strip()
		print("---\t{}".format(line))
		if line:
			if line[0] == '/':
				new_group['files'].append(line)
			else:
				new_group['file_size'] = int(line.split()[0])

		else:
			new_group = {'files':[]}
			redundant_files.append(new_group)
			continue


	redundant_files.sort(key=lambda group: group['file_size'], reverse=True)
	pprint(redundant_files)
