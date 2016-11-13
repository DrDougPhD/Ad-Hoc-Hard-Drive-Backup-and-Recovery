#!/usr/bin/env bash
#
# Set up a RAID 5 array.
#
# Based on the instructions provided in the ArchLinux RAID wiki page:
#		https://wiki.archlinux.org/index.php/RAID
#

# This script needs to be run as root.
if [[ $EUID -ne 0 ]]
then
	echo "This script must be run as root. Exiting." 
	exit 1
fi

THEMATIC_BREAK="-------------------------------------------------------------------------------"
PARTITIONS=("/dev/sdb1" "/dev/sdc1" "/dev/sdd1")

sudo mdadm --stop /dev/md0
sudo mdadm --remove /dev/md0
for drive in ${PARTITIONS[@]}
do
	sudo mdadm --zero-superblock ${drive}
done

