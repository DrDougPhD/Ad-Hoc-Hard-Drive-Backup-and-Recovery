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
drive="$1"
if [ -z $drive ]
then
	echo "Usage: test_drive_health.sh /dev/sdX"
	exit 1
fi


echo "Preliminary analysis of USB flash drive at '${drive}'"
echo "--------------------------------------------------------------------------------"

# Grab the sector size of the specified device.
drive_name=$( basename $drive )
sector_size=$(cat /sys/block/${drive_name}/queue/logical_block_size)
echo "Logical sector size: $sector_size bytes"

sudo badblocks -b ${sector_size}	\ # Specify the size of blocks in bytes.  The default is 1024.
	-o ${drive_name}.badblocks.txt	\ # Write the list of bad blocks to the specified file.  Without this option, badblocks displays the list on its standard output.  The format of this file is suitable for use by the -l option  in  e2fsck(8)  or mke2fs(8).
	-s	\ # Show  the progress of the scan by writing out rough percentage completion of the current badblocks pass over the disk.  Note that badblocks may do multiple test passes over the disk, in particular if the -p or -w option is requested by the user.
	-v	\ # Verbose mode.  Will write the number of read errors, write errors and data- corruptions to stderr.
	-w	\ # Use  write-mode  test.  With this option, badblocks scans for bad blocks by writing some patterns (0xaa, 0x55, 0xff, 0x00) on every block of the device, reading every block and comparing the contents.  This option may not be combined with the -n option, as they are mutually exclusive.


