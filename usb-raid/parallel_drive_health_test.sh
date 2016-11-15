#!/usr/bin/env bash
#
# Test a USB flash drive's health.
#
# Copyright 2016 Doug McGeehan. All rights reserved (for now).
#
#------------------------------------------------------------------------------
#
# TODO:
#

declare -a drives

function main {
	test_dependencies
	load_names_and_ids

	#parallel --jobs 0 --link ./health_test.sh :::: $DISK_NAMES_FILE :::: $DISK_IDENTIFIERS_FILE
}

function test_dependencies {
	parallel --version >/dev/null 2>&1 || { echo >&2 "GNU parallel is required but not installed. Aborting."; exit 1; }
	# TODO:
	# Perhaps instead of requiring parallel, I can fall back to a different approach?
	# 	http://stackoverflow.com/a/19543185
	# 		process1 &
	# 		process2 &
	# 		wait
	# 		process5 &
	# 		process6 &
	# 		wait
	# "Would you like to install now? [Y/n]: "
}

function load_names_and_ids {
	for devlink in /dev/disk/by-id/usb*
	do
		devpath=$( readlink -f ${devlink} )
		./health_test.sh ${devpath} &
	done
}

main

