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

DISK_NAMES_FILE=disk_names.fdisk.txt
DISK_IDENTIFIERS_FILE=disk_identifiers.fdisk.txt
declare -a drives
declare -a identifiers


function main {
	test_dependencies
	load_names_and_ids

	loop_index=0
	for drive in "${drives[@]}"
	do
		id=${identifiers[$loop_index]}
		echo "Drive: $drive, ID: $id"
		loop_index=$[$loop_index +1]
	done

	parallel --link echo :::: $DISK_NAMES_FILE :::: $DISK_IDENTIFIERS_FILE
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
	grep "Disk /" usb_drives.fdisk.txt | awk '{ print $2 }' | sed 's/://g' >${DISK_NAMES_FILE}
	grep "Disk identifier" usb_drives.fdisk.txt | awk '{ print $3 }' >${DISK_IDENTIFIERS_FILE}

	while read drive
	do
		drives+=( $drive )
	done < $DISK_NAMES_FILE

	while read id
	do
		identifiers+=( $id )
	done < $DISK_IDENTIFIERS_FILE
}

function test_health {
	drive=$1
	drive_name=$( basename $drive )
	identifier=$2
	echo "Preliminary analysis of USB flash drive at '${drive}'"
	echo "--------------------------------------------------------------------------------"

	# Grab the sector size of the specified device.
	sector_size=$(cat /sys/block/${drive_name}/queue/logical_block_size)
	echo "Logical sector size: $sector_size bytes"

	#sudo badblocks -b ${sector_size}	\
	#	-o ${drive_name}.badblocks.txt	\
	#	-s	\
	#	-v	\
	#	-w	\
	#	$drive
	#}
}

main

