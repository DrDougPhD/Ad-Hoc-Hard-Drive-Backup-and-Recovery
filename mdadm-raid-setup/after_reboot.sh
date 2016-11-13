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

DELAY=2

THEMATIC_BREAK="-------------------------------------------------------------------------------"
PARTITIONS=("/dev/sdb1" "/dev/sdc1" "/dev/sdd1")


#------------------------------------------------------------------------------
# Build the RAID 5 array.
#
CHUNK_SIZE=4096
./center_justify "=" "BUILD RAID ARRAY"
echo "Creating a RAID 5 array with chunk size of $CHUNK_SIZE on the following"
echo " partitions: ${PARTITIONS[*]}"
read -p "Press [ENTER] to continue: "
mdadm --create \
	--verbose \
	--level=5 \
	--metadata=1.2 \
	--chunk=${CHUNK_SIZE} \
	--raid-devices=3 \
	/dev/md0 \
	${PARTITIONS[*]}

#------------------------------------------------------------------------------
# Update the mdadm.conf configuration file.
#
echo "Writing out configuration to file"
echo 'DEVICE partitions' > ./mdadm.conf
mdadm --detail --scan >> ./mdadm.conf

#------------------------------------------------------------------------------
# Assemble the RAID 5 array.
#
echo "Assembling RAID 5 array"
read -p "Press [ENTER] to continue: "
mdadm --assemble --scan

#------------------------------------------------------------------------------
# Format the RAID filesystem.
#
./center_justify "=" "FILESYSTEM FORMATTING"
read -p "Press [ENTER] to continue: "
BLOCK_SIZE=4096
# stride = chunk size / block size
STRIDE=$(( CHUNK_SIZE / BLOCK_SIZE ))
# stripe width = number of data disks * stride
STRIPE_WIDTH=$(( STRIDE * (${#PARTITIONS[@]}-1) ))

function create_fs {
	mkfs.ext4 -v \
		-L myarray \
		-m 0 \
		-b ${BLOCK_SIZE} \
		-E stride=${STRIDE},stripe-width=${STRIPE_WIDTH} \
		/dev/md0
}

create_fs

