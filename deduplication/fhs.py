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
from collections import defaultdict

NOW = datetime.now()
_4MiB = 4*(1024**2)


def main():
	_ = Path('/')
	directory = _/'tmp'/'dupes'
	file = File.within(directory)('file.1')
	print(file)

from collections import deque
def lazy(method):
	"""
	Object methods decoraged by this decorator until an @eagor decorated
	method is called.
	"""
	eager_key = 'eager'
	def queuer(self, *args, **kwargs):
		if not hasattr(self, '_lazy_queue'):
			self._lazy_queue = deque()

		if eager_key in kwargs and kwargs[eager_key]:
			# if method was called eagerly, then execute it now
			# does not consider queue of methods to execute
			#return method(self, *args, **kwargs)
			print("Eager loading of lazy method: {method_name}".format(
				method_name=method.__name__
			))

		else:	# method will be queued for later execution
			print("Lazy loading of lazy method: {method_name}".format(
				method_name=method.__name__
			))
			if not hasattr(self, '_lazy_queue'):
				self._lazy_queue = []
			self._lazy_queue.append((method, args, kwargs))
	return queuer


def eager(method):
	"""
	Object methods decorated by this decorator triggers the execution of
	all lazy methods queued up prior.
	"""
	def resolve(queue, obj):
		for method, args, kwargs in queue:
			method(obj, *args, **kwargs)
		queue.clear()

	def evaluator(self, *args, **kwargs):
		print(thematic_break(char="~"))
		print("Eager evaluation started on method: {method_name}".format(
			method_name=method.__name__
		))
		if hasattr(self, '_lazy_queue') and self._lazy_queue:
			resolve(queue=self._lazy_queue, obj=self)
		return method(self, *args, **kwargs)
	return evaluator

def cascade(method):
	"""
	Decorator for non-invasively implementing the Method cascading pattern.
	Read more: https://en.wikipedia.org/wiki/Method_chaining
	"""
	def calling_object_returner(self, *args, **kwargs):
		method(self, *args, **kwargs)
		return self

	return calling_object_returner


class File:
	BLOCKSIZE=_4MiB

	@staticmethod
	def within(directory):
		print("walking through files within '{directory}'".format(
			directory=directory
		))
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
		return self.path.stat().st_size

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
		return File(self.path/key)

	def __rtruediv__(self, key):
		return File(key/self.path)

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
	"""
	The bundling key needs to operate such that it defines an equivalence
	relation on files. In other words, the bundling key should partition
	the set of files. This partitioning creates equivalence classes called
	"bundles" such that any two files within a bundle have the same value
	of the key produced by the bundling key. Thus, the FileBundles object
	can be seen as a quotient set of its constituent files by the
	bundling-key equivalence relation.
	"""
	@lazy
	def __init__(self, within, key):
		"""
		Recursively walk through all files stored within the specified
		root directory and bundle them together based on the output
		of a specified function.
		"""
		print("...(actually executing: FileBundles.__init__)...")
		self.within = within
		self.bundle_key = key
		self.file_bundles = []

		self.file_bundles = defaultdict(list)
		for directory, _, files in os.walk(str(within)): #, topdown=False):
			if not files:
				print("\t no files, skipping '{directory}'".format(directory=directory))
				print("."*80)
				continue

			for file in map(File.within(directory), files):
				print("\t{file}".format(file=file))
				self.file_bundles[len(file)].append(file)
				print("... bundles updated with '{file}'".format(file=file))
				pprint.pprint(self.file_bundles)
				if len(self.file_bundles[len(file)]) > 1:
					# apply second bundling?
					pass
			print("."*80)

	@cascade
	@lazy
	def filter(self, function):
		"""
		Filter out file bundles based on this function's truthiness.
		"""
		print("...(filter)...")
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

	@eager
	def __str__(self):
		return pprint.pformat(self.file_bundles)


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
	"""
	duplicate_files = FileBundles(within=directory, key=os.path.getsize)\
		.filter(by=only_multifile_bundles)\
		.hone(by=hash)\
		.filter(by=only_multifile_bundles)\
		.sort(key=size_reduction_from_pruning, reversed=True)\
		.apply(fn=sort_by_descending_age)\
		.apply(fn=hide_oldest)

	print(format(
		value=duplicate_files.annotate(with_=storage_space_running_total),
		format_spec=("{truncated_path:>20}\t{humanized_size:>5}\t"
			"{age:>10}\t{storage_space_running_total:>5}")
	))
	"""

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

	print(thematic_break(title="STAGE 2", char="="))
	print(thematic_break(title="remove singleton file bundles"))
	only_multifile_bundles = lambda bundle: 1 < len(bundle)
	#potential_duplicates = filter(only_multifile_bundles, files)
	potential_duplicates = files.filter(only_multifile_bundles)
	print(potential_duplicates)
	print(thematic_break())

	"""
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

