import humanize
import os
import argparse
from pathlib import Path

def truncate_url(path, to_length=70):
	dirname, filename = os.path.split(path)
	filename_length = len(filename)
	path_parts = dirname.split('/')
	dirname += '/'
	
	while to_length < len(dirname)+filename_length:
		path_parts = path_parts[1:]
		dirname = '.../' + '/'.join(path_parts) + '/'
		if not path_parts:
			dirname = dirname[:-1] # remove trailing slash "..//"
			break

	# if filename is still to long...
	path_length = len(dirname)+filename_length
	if to_length < path_length:
		filename_elipses = "[...]"
		filestem, fileext = os.path.splitext(filename)
		reduce_by = path_length - (to_length - len(filename_elipses))
		filename = filestem[:-reduce_by].strip() + filename_elipses + fileext
		assert len(filename) <= to_length, "not short enough"

	return dirname + filename


def get_arguments():
	parser = argparse.ArgumentParser(
		description=("Construct a shell script to delete duplicate "
			"files, potentially replacing them with symbolic "
			"links")
	)
	parser.add_argument('-v', '--verbose', action='store_true',
		default=True, help='verbose output')
	parser.add_argument('-d', '--within-directory',
		dest='within_directory',
		default='.', type=Path,
		help='path to directory in which to search for dupes',
	)
	parser.add_argument('-f', '--fdupes-file',
		dest='fdupes_file', type=Path,
		required=True,
		help='pre-existing fdupes file with filesizes',
	)
	parser.add_argument('-g', '--space-recovery-goal',
		dest='bytes_to_reclaim',
		help=('How much space is desired to be reclaimed. '
			'Delete enough files to reach this goal.'),
		default=float('inf')
	)
	parser.add_argument('-s', '--replace-with-symlinks',
		dest='replace_with_symlinks', action='store_true',
		default=False,
		help="instead of outright deleting, replace files with symlinks"
	)
	parser.add_argument('-m', '--min-duplicate-size-to-delete',
		dest='min_dupe_group_size',
		default=0, type=int,
		help='groups taking up less than this size will not be deleted',
	)

	return parser.parse_args()

args = get_arguments()
with open(str(args.fdupes_file)) as f:
	redundant_files = []
	for line in f:
		line = line.strip()
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
	large_enough_savings = lambda grp: grp['savings_if_deduped'] > args.min_dupe_group_size

	# summarize the files that would be deleted, along with how much space
	# is reclaimed by deleting all files above that line
	print('#'*80)
	print("# {path:^60}  {size:^6}  {savings:^6} #".format(
		path="Files to delete (truncated paths)",
		size="Size",
		savings="Save"
	))

	running_total_savings = 0
	duplicates = list( filter(large_enough_savings, redundant_files) )
	try:
		for duplicate_group in duplicates:
			files_to_delete = duplicate_group['files'][1:]
			for file in files_to_delete:
				running_total_savings += duplicate_group['file_size']
				print("# {path:>60}  {size:>6}  {running_total_savings:>6} #".format(
					path=truncate_url(file, to_length=60),
					size=humanize.naturalsize(
						duplicate_group['file_size'],
						gnu=True
					),
					running_total_savings=humanize.naturalsize(
						running_total_savings,
						gnu=True
				)))
				if running_total_savings >= args.bytes_to_reclaim:
					raise
	except: # no need to continue iterating once goal is reached
		pass

	print('#'*80)

	running_total_savings = 0
	try:
		# create shell commands to perform deletion
		for duplicate_group in filter(large_enough_savings, redundant_files):
			original_file = duplicate_group['files'][0]
			print("#"*40 + " Original: '{}'".format(original_file))
			files_to_delete = duplicate_group['files'][1:]
			for file in files_to_delete:
				running_total_savings += duplicate_group['file_size']
				print("rm '{}'".format(file))
				if args.replace_with_symlinks:
					print("ln -s '{original_file}' '{deleted_file_path}'".format(
						original_file=original_file,
						deleted_file_path=file,
					))
				if running_total_savings >= args.bytes_to_reclaim:
					raise

	except:
		pass

