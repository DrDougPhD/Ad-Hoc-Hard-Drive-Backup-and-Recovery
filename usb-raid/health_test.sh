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

THIN_THEMATIC_BREAK="-------------------------------------------------------------------------------\n"
THICK_THEMATIC_BREAK="================================================================================\n"


echo -e "Preliminary analysis of USB flash drive at '${drive}'\n"\
"Logical sector size: $sector_size bytes\n"\
$THIN_THEMATIC_BREAK

#sudo badblocks -b ${sector_size}	\
#	-o ${drive_name}.badblocks.txt	\
#	-s	\
#	-v	\
#	-w	\
#	$drive
#}


