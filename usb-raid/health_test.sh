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
THIN_THEMATIC_BREAK="-------------------------------------------------------------------------------"
THICK_THEMATIC_BREAK="==============================================================================="

devpath=$1
if [ -z $devpath ]
then
	echo "Usage: [bash] health_test.sh /dev/sdX"
fi

devname=$( basename $devpath )
devserial=$( udevadm info -p /sys/class/block/${devname}/ --query=property | grep 'ID_SERIAL_SHORT' | awk -F"=" '{ print $2 }'  )
if [ -z $devserial ]
then
	devserial="NoUUID"
fi

sector_size=$(cat /sys/block/${devname}/queue/logical_block_size)
sector_count=$(cat /sys/block/${devname}/size)
byte_size=$(( $sector_count * $sector_size ))
human_size=$( numfmt --to=si --suffix=B --format="%.1f" $byte_size )

# human size; device name; serial; bytesize; sector size; sector count; device link
echo -e "${human_size}\t${devname}\t${devserial}\t${byte_size}\t${sector_size}\t${sector_count}" >>${DRIVE_INFO_FILE}
echo $THICK_THEMATIC_BREAK
echo "${human_size} USB drive at '${devpath}'"
echo "Unique ID / Serial number: ${devserial}"
echo "Logical sector size: $sector_size bytes"
echo "Drive capacity: $human_size, $byte_size bytes"
echo $THIN_THEMATIC_BREAK

function tester {
	sudo badblocks -b ${sector_size}	\
		-o ${devserial}.${devname}._${human_size}_.badblocks.txt	\
		-s	\
		-w	\
		$devpath
}

tester

