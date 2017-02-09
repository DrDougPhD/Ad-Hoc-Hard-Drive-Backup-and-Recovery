#!/usr/bin/env python3
"""

TODO
	* For .img files, attempt to mount them and traverse through the files
	  stored within.
		* Some of these .img files are entire hard drive images, while others are
		  partitions.
		* A more sophisticated strategy for mounting them may be necessary, such
		  as creating a mount script to accompany those files.
	* Show average and standard deviation of file-sizes for each extension as
		a command-line graph
			e.g.
				filesizes:  1K  10K  100K  1M  10M  100M  1G  10G  100G  1T
				         +-------------------------------------------------------------
				    .mkv |               ----+++++#++++----
				    .avi |                     --++#++--
				   .flac |                 --++#++--
				         +-------------------------------------------------------------
	* Show total consumed space per file-size as a command-line graph
			e.g.
				 occupied:  1K  10K  100K  1M  10M  100M  1G  10G  100G  1T  10T
				         +-------------------------------------------------------------
				    .mkv |                                                 #     5.2 TB
				    .avi |                                            #         30.4 GB
				   .flac |                                    #                100.2 GB
				         +-------------------------------------------------------------
	* Possible libraries to use:
		* https://github.com/mkaz/termgraph
		* https://github.com/glamp/bashplotlib

"""

import os
import sys
from collections import defaultdict
from pprint import pprint

###############################################################################
"""
from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo=True)

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class File(Base):
	__tablename__ = 'files'
	id = Column(Integer, primary_key=True)
	directory_id = Column(Integer, ForeignKey('directories.id'))
	directory = relationship('Directory', back_populates='path')
	filename = Column(String)
	extension = Column(String)

	def __repr__(self):
		return 'stuff'


Directory.files = relationship(
	'File', back_populates='filename'
)


class Directory(Base):
	__tablename__ = 'directories'
	id = Column(Integer, primary_key=True)
	path = Column(String)
	files_id = Column(Integer, ForeignKey('files.id'))
	files = relationship('File', back_populates='filename')

	def __repr__(self):
		return 'stuff'


Base.metadata.create_all(engine)

###############################################################################
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()
"""

def count_file_types_within(directory_to_walk):
	file_type_counts = defaultdict(int)

	for dirpath, _, filenames in os.walk(directory_to_walk):
		for file in filenames:
			file_prefix, file_extension = os.path.splitext(file)

			if file_extension == "":
				file_extension = "(none)"

			file_type_counts[file_extension.lower()] += 1

	return sorted(
		[(ext, file_type_counts[ext]) for ext in file_type_counts],
		key=lambda t: t[1],
		reverse=True
	)


def write_counts_to_stdout(file_type_counts):
	# iterate over file extensions and measure the widest one, for pretty
	# printing
	max_width_extension = max(
		file_type_counts,
		key=lambda c: len(c[0])
	)[0]
	max_width = len(max_width_extension)

	for ext_count in file_type_counts:
		print("{0}:\t{1}".format(ext_count[0].rjust(max_width), ext_count[1]))


if __name__ == "__main__":
	directory_to_walk = sys.argv[-1]
	file_type_counts = count_file_types_within(directory_to_walk)
	write_counts_to_stdout(file_type_counts)

