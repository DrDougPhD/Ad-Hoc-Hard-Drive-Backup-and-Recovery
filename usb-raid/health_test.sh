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

drive=$1
drive_name=$( basename $drive )
identifier=$2
sector_size=$(cat /sys/block/${drive_name}/queue/logical_block_size)
sector_count=$(cat /sys/block/${drive_name}/size)
byte_size=$(( $sector_count * $sector_size ))
human_size=$( numfmt --to=si --suffix=B --format="%.1f" $byte_size )

THIN_THEMATIC_BREAK="-------------------------------------------------------------------------------\n"
THICK_THEMATIC_BREAK="================================================================================\n"


echo -e "Preliminary analysis of USB flash drive at '${drive}'\n"\
"Unique ID: ${identifier}\n"\
"Logical sector size: $sector_size bytes\n"\
"Drive capacity: $human_size, $byte_size bytes\n"\
$THIN_THEMATIC_BREAK

function tester {
	sudo badblocks -b ${sector_size}	\
		-o ${identifier}.${drive_name}._${human_size}_.badblocks.txt	\
		-s	\
		-w	\
		$drive
}

