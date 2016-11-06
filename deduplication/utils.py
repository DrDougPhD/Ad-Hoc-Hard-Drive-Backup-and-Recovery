"""
Collection of utilities useful for this project.
"""

import os
import errno
import logging
import config
from dateutil.parser import parse


def create_directory_safely(path):
	"""
	Try to create a directory, but ignore an error pertaining to it already
	existing.
	Source: http://stackoverflow.com/a/5032238
	"""
	try:
		os.makedirs(path)

	except OSError as exception:
		if exception.errno != errno.EEXIST:
			raise


# There's a better, more pythonic way of accomplishing this.
def get_descendant_logger(descendant_name):
	if descendant_name == "__main__":
		# set up basic logger
		logging.basicConfig(level=logging.DEBUG)
		logger = logging.getLogger("testing")

	else:
		# set up descendant logger
		logger = logging.getLogger("{0}.{1}".format(
			config.APP_NAME,
			descendant_name
		))

	return logger


"""
def string2datatype(value):
	if value.lower() == "true":
		return True

	if value.lower() == "false":
		return False

	if value == "":
		return None

	# moving on to the trial and error conversions
	try:
		return int(value)

	except:
		pass

	try:
		return parse(value)
	except:
		pass

	# after all failures, just return a string
	return str(value)
"""
