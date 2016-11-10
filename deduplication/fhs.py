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
	assert len(line)==width, "Line length is not of expected length (expected: {width}, actual: {line_width})\n{line}".format(width=width, line_width=len(line), line=line)
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

	"""
	only_multifile_bundles = lambda bundle: 1 < len(bundle)
	#potential_duplicates = filter(only_multifile_bundles, files)
	potential_duplicates = files.filter(only_multifile_bundles)
	print(potential_duplicates)

	print(filehasher(file_path=directory/'file.1'))
	hashed_files = FileBundler(
		within=potential_duplicates,
		key=filehasher
	)
	duplicate_files = hashed_files.filter(only_multifile_bundles)
	""" 
