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
DRIVES=("sdb" "sdc" "sdd")


#------------------------------------------------------------------------------
# Install software dependencies.
#
install_dependencies () {
	apt-get install -y mdadm gdisk
}
#install_dependencies

#------------------------------------------------------------------------------
# Double-check that hard drives to be added to the array are not currently
# mounted.
#		* Check lsblk or something else
#		* Ask user to select drives from interactive prompt
#		* Ask user to confirm
#
confirm () {	# copied from http://stackoverflow.com/a/3232082
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
	./center_justify "=" "INFORMATION ON DRIVE /dev/${drive}"
	smartctl -i "/dev/${drive}"
done
echo 

lsblk
echo $THEMATIC_BREAK

echo "Drives to process:"
for drive in ${DRIVES[@]}
do
	echo -e "\t/dev/${drive}"
done
echo "Are you sure you want to go through this data-"
echo "destroying process on the aforementioned drives?"
confirm

# if the script has made it this far, the user entered some variant of "Yes"

#------------------------------------------------------------------------------
# Prepare the drives by clearing their superblocks.
#
for drive in ${DRIVES[@]}
do
	echo "Erasing superblock on /dev/${drive}"
	# mdadm --zero-superblock /dev/${drive}
	echo $THEMATIC_BREAK
done

#------------------------------------------------------------------------------
# Create the partition table - GPT
#

