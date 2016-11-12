#!/usr/bin/env bash
# Set up a RAID 5 array

THEMATIC_BREAK="-------------------------------------------------------------------------------"

# This script needs to be run as root.
if [[ $EUID -ne 0 ]]
then
	echo "This script must be run as root. Exiting." 
	exit 1
fi

install_dependencies ()
{	# Install mdadm
	apt-get install -y mdadm
}
#install_dependencies

# Double-check that hard drives to be added to the array are not currently
# mounted.

DRIVES=("sdb" "sdc" "sdd")
for drive in ${DRIVES[@]}
do
	echo "Erasing superblock on /dev/${drive}"
	# mdadm --zero-superblock /dev/${drive}
	echo $THEMATIC_BREAK
done
