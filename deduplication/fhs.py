"""
A Python library for representing file paths in the Filesystem Hierarchy
Standard.

The classes in this file are designed for functionality of the project that
imports this.
"""

from pathlib import Path
import os.path
import hashlib
import math


_4MiB = 4*(1024**2)


class FileBundler:
	def __init__(self, within, key):
		"""
		Recursively walk through all files stored within the specified
		root directory and bundle them together based on the output
		of a specified function.
		"""
		self.file_bundles = []

	def filter(self, function):
		return self

	def __lt__(self, other):
		return len(self) < len(other)

	def overhead(self):
		pass

	"""
	def __iter__(self):
		for bundle in self.file_bundles:
			yield bundle

	def __str__(self):
		return self
	"""


def filehasher(file_path, block_size=_4MiB):
	assert file_path.exists(), "File not found - '{file_path}'".format(file_path=file_path)
	file_path = str(file_path)
	hasher = hashlib.md5()

	with open(file_path, 'rb') as file:
		while True:
			block = file.read(block_size)
			if len(block)==0:
				break
			hasher.update(block)

	return hasher.hexdigest()


def thematic_break(title=None, char='-', width=80):
	#TODO: if len("- " + title + " -") > width, then split in half nicely
	if not title:
		return char*width

	title = str(title).strip()
	half_title_length = math.ceil( len(title)/2 )
	buffer_width_from_center = half_title_length+1

	half_width = width // 2
	half_break_length = half_width - buffer_width_from_center

	line = '{dashes} {title} {dashes}'.format(
		dashes=char*half_break_length,
		title=title
	)
	if len(line)==(width-1):
		line += char
	assert len(line)==width, ("Line length is not of expected length "
		"(expected: {width}, actual: {line_width})\n{line}".format(
		width=width, line_width=len(line), line=line))
	return line


if __name__ == "__main__":
	print("Testing the fhs module")

	print(thematic_break(title="STAGE 1", char="="))
	print(thematic_break(title="file system walking", char="-"))
	_ = Path('/')
	directory = _/'tmp'/'dupes'
	files = FileBundler(
		within=directory,
		key=os.path.getsize
	)
	print(files)
	print(thematic_break())

	print(thematic_break(title="STAGE 2", char="="))
	print(thematic_break(title="remove singleton file bundles"))
	only_multifile_bundles = lambda bundle: 1 < len(bundle)
	#potential_duplicates = filter(only_multifile_bundles, files)
	potential_duplicates = files.filter(only_multifile_bundles)
	print(potential_duplicates)
	print(thematic_break())

	print(thematic_break(title="STAGE 3", char="="))
	print(thematic_break(title="compute file hashes", char="-"))
	hashed_files = FileBundler(
		within=potential_duplicates,
		key=hash
	)
	print(potential_duplicates)
	print(thematic_break())


	print(thematic_break(title="STAGE 4", char="="))
	print(thematic_break(title="focus on files with duplicate copies"))
	duplicate_files = hashed_files.filter(only_multifile_bundles)
	print(duplicate_files)
	print(thematic_break())
	#print(filehasher(file_path=directory/'file.1'))

	print(thematic_break(title="STAGE 5", char="="))
	print(thematic_break(
		title="sort bundles by size reduction through pruning",
	))
	size_reduction_from_pruning = lambda bundle: bundle
	sorted_bundles_of_duplicate_file = sorted(
		duplicate_files, key=redundancy_overhead, reversed=True
	)
	print(sorted_dupes)
	print(thematic_break())

	print(thematic_break(title="STAGE 6", char="="))
	print(thematic_break(title="sort by file age within each bundle"))
	sort_bundle_by_file_age = lambda bundle: sorted(bundle, key=blah)

	further_sorted_by_file_age = map(
		sort_bundle_by_file_age,
		sorted_bundles_of_duplicate_files,
	)
	print(sorted_dupes)
	print(thematic_break())

	#--- list files to delete?
	# #original :=> size, age, truncated_url, 3 duplicate copies
	for bundle in further_sorted_by_file_age:
		print(bundle.summary())

		for file in bundle:
			if file == bundle.oldest():
				print("# original :=> {truncated_url} ({size}, {age}), {n} duplicate copies".format(
					truncated_url=file.truncate_url(),
					size=len(file),
					age=file.age(),
					n=len(bundle)-1
				))
			else:
				print("{truncated_url}\t{size}\t{age}\t{space_recovered}",
					space_recovered=cum_size_reduction_if_deleted,
					size=len(file),
					age=file.age(),
					truncated_url=file.truncate_url()
				)

	# cumulative_size, age, truncated_url
#hash(obj)

