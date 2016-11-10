"""
A Python library for representing file paths in the Filesystem Hierarchy
Standard.

The classes in this file are designed for functionality of the project that
imports this.
"""

from pathlib import Path
import os.path
import hashlib


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
	"""

	def __str__(self):
		return (
			"-"*30 + "FileBundler" + "-"*30
		)


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


if __name__ == "__main__":
	print("Testing the fhs module")

	_ = Path('/')
	directory = _/'tmp'/'dupes'

	files = FileBundler(
		within=directory,
		key=os.path.getsize
	)
	print(files)

	only_multifile_bundles = lambda bundle: 1 < len(bundle)
	#potential_duplicates = filter(only_multifile_bundles, files)
	potential_duplicates = files.filter(only_multifile_bundles)
	print(potential_duplicates)

	print(filehasher(file_path=directory/'file.1'))
	"""
	actual_duplicates = FileBundler(
		within=potential_duplicates,
		key=hash_fn
	)
	"""
