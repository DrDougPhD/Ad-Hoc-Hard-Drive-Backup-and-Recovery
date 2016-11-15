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

DRIVE_INFO_FILE=usb_disks.info.txt
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
		devname=$( basename $devpath )
		devserial=$( udevadm info -p /sys/class/block/${devname}/ --query=property | grep 'ID_SERIAL_SHORT' | awk -F"=" '{ print $2 }'  )
		sector_size=$(cat /sys/block/${devname}/queue/logical_block_size)
		sector_count=$(cat /sys/block/${devname}/size)
		byte_size=$(( $sector_count * $sector_size ))
		human_size=$( numfmt --to=si --suffix=B --format="%.1f" $byte_size )
		# human size; device name; serial; bytesize; sector size; sector count; device link
		echo -e "${human_size}\t${devname}\t${devserial}\t${byte_size}\t${sector_size}\t${sector_count}\t${devlink}" >>${DRIVE_INFO_FILE}
		echo "${human_size} USB drive at '${devpath}'"
	done
}

main

