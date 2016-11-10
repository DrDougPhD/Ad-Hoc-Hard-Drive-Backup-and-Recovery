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
from datetime import datetime
import pprint


NOW = datetime.now()
_4MiB = 4*(1024**2)


def main():
	_ = Path('/')
	directory = _/'tmp'/'dupes'
	file = File.within(directory)('file.1')
	print(file)


def lazy(fn):
	def loader(self, *args, **kwargs):
		self._load()
		return fn(self, *args, **kwargs)
	return loader


class File:
	BLOCKSIZE=_4MiB

	@staticmethod
	def within(directory):
		blank_file_within_directory = File(directory)
		def build_from_filename(filename):
			return blank_file_within_directory/filename

		return build_from_filename

	def __init__(self, path):
		if isinstance(path, str):
			self.path = Path(path)
		else:
			self.path = path

	def age(self):
		mtime = datetime.fromtimestamp(self.stat().st_mtime)
		age = NOW - mtime
		return str(age)

	def __len__(self):
		return self.stat().st_size

	def truncated_path(self):
		return str(self)

	def __hash__(self):
		assert self.exists(), "File not found - '{file_path}'".format(
			file_path=self)
		assert self.is_file(), "Not a file - '{file_path}'".format(
			file_path=self)
		hasher = hashlib.md5()

		with open(str(file_path), 'rb') as file:
			while True:
				block = file.read(File.BLOCKSIZE)
				if len(block)==0:
					break
				hasher.update(block)

		return hasher.hexdigest()

	def _load(self):
		pass

	def __truediv__(self, key):
		self.path = self.path/key
		return self

	def __rtruediv__(self, key):
		self.path = key/self.path
		return self

	def __repr__(self):
		return str(self.path)


class FileBundle:
	def __init__(self):
		pass

	def oldest(self):
		pass

	def __iter__(self):
		for file in self.bundle:
			yield file


class FileBundles:
	def __init__(self, within, key):
		"""
		Recursively walk through all files stored within the specified
		root directory and bundle them together based on the output
		of a specified function.
		"""
		self.within = within
		self.bundle_key = key
		self.file_bundles = []
		self.files = []

	def filter(self, function):
		return self

	def __lt__(self, other):
		return len(self) < len(other)

	def overhead(self):
		pass

	def __radd__(self, other):
		if other == 0:
			return self
		else:
			return self.__add__(other)

	def __add__(self, other):
		pass

	"""
	def __iter__(self):
		for bundle in self.file_bundles:
			yield bundle

	"""

	def _load(self):
		within_path = str(self.within)
		for directory, _, files in os.walk(within_path, topdown=False):
			self.files.extend(map(File.within(directory), files))

	@lazy
	def __str__(self):
		return pprint.pformat(self.files)


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
	#main()

	print(thematic_break(title="STAGE 1", char="="))
	print(thematic_break(title="file system walking", char="-"))
	_ = Path('/')
	directory = _/'tmp'/'dupes'
	files = FileBundles(
		within=directory,
		key=os.path.getsize
	)
	print(files)
	print(thematic_break())

	"""
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
		duplicate_files,
		key=size_reduction_from_pruning,
		reversed=True
	)
	print(sorted_bundles_of_duplicate_file)
	print(thematic_break())

	print(thematic_break(title="STAGE 6", char="="))
	print(thematic_break(title="sort by file age within each bundle"))
	sort_bundle_by_file_age = lambda bundle: sorted(
		bundle, key=lambda file: file.stat().st_mtime
	)
	further_sorted_by_file_age = map(
		sort_bundle_by_file_age,
		sorted_bundles_of_duplicate_files,
	)
	print(sorted_dupes)
	print(thematic_break())

	#--- list files to delete?
	# #original :=> size, age, truncated_url, 3 duplicate copies
	cum_size_reduction_if_deleted = 0
	for bundle in further_sorted_by_file_age:
		for file in bundle:
			if file == bundle.oldest():
				print("# original :=> {truncated_url} ({size}, {age}), {n} duplicate copies".format(
					truncated_url=file.truncate_url(),
					size=len(file),
					age=file.age(),
					n=len(bundle)-1
				))
			else:
				cum_size_reduction_if_deleted += file
				print("{truncated_url}\t{size}\t{age}\t{space_recovered}",
					space_recovered=cum_size_reduction_if_deleted,
					size=len(file),
					age=file.age(),
					truncated_url=file.truncate_url()
				)
	"""
	# cumulative_size, age, truncated_url
#hash(obj)

