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
DRIVES=("/dev/sdb" "/dev/sdc" "/dev/sdd")


#------------------------------------------------------------------------------
# Install software dependencies.
#
function install_dependencies {
	apt-get install -y mdadm gdisk smartmontools
}
./center_justify "=" "INSTALL DEPENDENCIES"
install_dependencies
sleep $DELAY

#------------------------------------------------------------------------------
# Double-check that hard drives to be added to the array are not currently
# mounted.
#		* Check lsblk or something else
#		* Ask user to select drives from interactive prompt
#		* Ask user to confirm
#
function confirm {	# copied from http://stackoverflow.com/a/3232082
	# call with a prompt string or use a default
	read -r -p "${1:-Response} [y/N]: " response
	case $response in
		[yY][eE][sS]|[yY]) 
			true
			;;
		*)
			exit
			;;
	esac
}

for drive in ${DRIVES[@]}
do
	./center_justify "-" "INFORMATION ON DRIVE ${drive}"
	smartctl -i "${drive}"
	sleep $DELAY
done
echo 

lsblk
echo $THEMATIC_BREAK
sleep $DELAY

echo "Drives to process:"
for drive in ${DRIVES[@]}
do
	echo -e "\t ${drive}"
done
echo "Are you sure you want to go through this data-"
echo "destroying process on the aforementioned drives?"
confirm

# if the script made it this far, then the user entered some variant of "Yes"

#------------------------------------------------------------------------------
# Prepare the drives by clearing their superblocks.
#
for drive in ${DRIVES[@]}
do
	echo "Erasing superblock on ${drive}"
	mdadm --zero-superblock ${drive}
	echo $THEMATIC_BREAK
	sleep $DELAY
done

#------------------------------------------------------------------------------
# Create the partition table - GPT
#
# TODO: Since I have practically a different hard drive manufacturer on each
#  disk, it is prudent that the partition sizes all be equal. Thus, the
#  partition sizes should all be equal to the disk with the smallest sector
#  count.
#
# TODO: Disk / parition label should reflect something unique to the drive.
#  I would like to set their names as the drive family, model, and serial
#  number, which are obtainable by calling:
#		# smartctl -i /dev/${drive}
#  I don't know if that format of a drive name is too long.
#
SGDISK_LINUX_RAID_TYPECODE="fd00"
MIN_END_SECTOR=""
function update_min {
	# Return the minimum value of the two parameters.
	if [ -z "${MIN_END_SECTOR}" ]
	then	# minimum holder is not set, so let's set it with this value
		MIN_END_SECTOR=$1
	fi

	MIN_END_SECTOR=$(( $1<$MIN_END_SECTOR ? $1 : $MIN_END_SECTOR ))
}

# Create GPT partition tables on each drive, and determine the minimum ending
# sector boundary over all drives.
./center_justify "+" "CREATING PARTITION TABLES"
for drive in ${DRIVES[@]}
do
	# Erase all GPT data structures and create a fresh GPT.
	sgdisk --clear ${drive}
	# 	Display the sector number at the end of the largest empty block of sectors on the disk.
	update_min $(sgdisk --end-of-largest ${drive})
done
echo "End sector number is at ${MIN_END_SECTOR}."

#------------------------------------------------------------------------------
# Create partitions on each drive.
#
declare -a PARTITIONS
INDEX=0
function partition {
	# Read more on sgdisk here:
	#		http://www.rodsbooks.com/gdisk/sgdisk-walkthrough.html

	drive="$1"
	echo "Creating partition for '${drive}'"

	# Gather information about first and last sector of the disk.
	# 	Display the sector number of the first usable sector of the largest empty block of sectors on the disk, after partition alignment is considered.
	BEGINSECTOR=$(sgdisk --first-aligned-in-largest ${drive})

	# When replacing a failed disk of a RAID, the new disk has to be exactly the
	#	 same size as the failed disk or bigger, otherwise the array recreation
  #  process will not work. Even hard drives of the same manufacturer and model
  #  can have small size differences. By leaving a little space at the end of
  #  the disk unallocated one can compensate for the size differences between
  #  drives, which makes choosing a replacement drive model easier. Therefore,
	#  it is good practice to leave about 100 MB of unallocated space at the end
  #  of the disk.
	# TODO: Iterate through disks, obtaining smallest sector value.
	#       Take smallest sector value and subtract 100 MB from it.
	#       Use that amount for the disk partition's end-sector value.

	# Create the new partition and write it to the disk.
	# 	--new, args=partnum:start:end, Create a new partition, numbered partnum, starting at sector start and ending at sector end.
	# 	--change-name, args=partnum:name, Change the name of the specified partition.
	# 	--typecode, args=partnum:hexcode, Change a partition's GUID type code to the one specified by hexcode. Note that hexcode is a gdisk/sgdisk internal two-byte hexadecimal code. You can obtain a list of codes with the -L option.
	label=$(smartctl -i ${drive} | ./make_model_serial)
	echo "Partition to be named '$label'"
	sgdisk	--new					1:${BEGINSECTOR}:${MIN_END_SECTOR} \
					--change-name	1:"${label}" \
					--typecode		1:${SGDISK_LINUX_RAID_TYPECODE}	\
					${drive}

	# Print information about the newly-partitioned disk.
	sgdisk -p ${drive}

	PARTITIONS[${INDEX}]="${drive}1"
	INDEX=$(( 1 + ${INDEX} ))
}

./center_justify "=" "CREATING PARTITIONS"
# Create partitions on each drive with appropriate size and labels.
for drive in ${DRIVES[@]}
do
	disk="${drive}"
	partition ${drive}
	echo $THEMATIC_BREAK
done
sleep $DELAY

#------------------------------------------------------------------------------
# Build the RAID 5 array.
#
CHUNK_SIZE=4096
./center_justify "=" "BUILD RAID ARRAY"
echo "Creating a RAID 5 array with chunk size of $CHUNK_SIZE on the following"
echo " partitions: ${PARTITIONS[*]}"
sleep $DELAY
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
sleep $DELAY
mdadm --detail --scan >> ./mdadm.conf
sleep $DELAY

#------------------------------------------------------------------------------
# Assemble the RAID 5 array.
#
echo "Assembling RAID 5 array"
sleep $DELAY
mdadm --assemble --scan

#------------------------------------------------------------------------------
# Format the RAID filesystem.
#
./center_justify "=" "FILESYSTEM FORMATTING"
sleep $DELAY
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

