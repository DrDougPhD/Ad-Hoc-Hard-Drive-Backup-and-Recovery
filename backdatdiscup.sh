#!/usr/bin/env bash
#
# TODO
#	Detect if inserted disc is a music CD
#	Continuously loop until disc is inserted and ready
#	Detect when blank disc is inserted and notify user
#	When image has been duplicated, mount image and copy files to secondary
#		location.
#
USER_PROMPT="Enter CD name and press [ENTER]: "
INFO_DIR="info"
IMG_DIR="img"
LOG_DIR="log"
SECONDARY_DST="/media/kp/AB58-B7AF/CD Backups"

EMPTY_DRIVE=0
BLANK_DISC=2048

mkdir -p "${INFO_DIR}"
mkdir -p "${IMG_DIR}"
mkdir -p "${LOG_DIR}"

echo -n "${USER_PROMPT}"

while read cd_name
do
	# check if nothing was input
	if [[ -z "${cd_name// }" ]]
	then
		exit
	fi

	# wait until disc is ready
	echo "Waiting for disc"
	cd_drive_size=$EMPTY_DRIVE
	while [[ $cd_drive_size -le $BLANK_DISC ]]
	do
		echo -ne "."
		cd_drive_size=$(udisksctl info --block-device /dev/sr0 | grep 'Size:' | awk -F' ' '{ print $2 }' -)
		if	[[ $cd_drive_size -eq $EMPTY_DRIVE ]]
		then
			sleep 1
		elif	[[ $cd_drive_size -eq $BLANK_DISC ]]
		then
			echo
			echo "Blank disc in drive. Ejecting."
			eject /dev/sr0
			sleep 1
			cd_drive_size=$EMPTY_DRIVE
		else
			echo
			echo "Disc found! Begin mirroring."
		fi
	done

	# gather metadata and begin mirroring
	blkid /dev/sr0			>"${INFO_DIR}/${cd_name}.blkid.txt"
	udisksctl info --block-device /dev/sr0 \
					>"${INFO_DIR}/${cd_name}.udisks.txt"
	isoinfo -p -d -i /dev/sr0	>"${INFO_DIR}/${cd_name}.isoinfo.txt"
	ddrescue	--no-scrape \
			--sector-size=2048				\
			/dev/sr0					\
			"${IMG_DIR}/${cd_name}.img" \
			"${LOG_DIR}/${cd_name}.ddrescue.log"
	eject /dev/sr0 & # copying might take a while, so don't allow eject to block
	echo "------------------= copy files to secondary  =------------------"
	mkdir -p ~/mirror_img
	mount -o loop,ro "${IMG_DIR}/${cd_name}.img" ~/mirror_img && \
	rsync -rltzuv ~/mirror_img/ "${SECONDARY_DST}/${cd_name}" && \
	umount ~/mirror_img

	echo "------------------= done done done done done =------------------"
	echo -n "${USER_PROMPT} "
done < "${1:-/dev/stdin}"
