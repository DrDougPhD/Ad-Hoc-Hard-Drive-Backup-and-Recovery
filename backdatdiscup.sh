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
TMP_DIR=".tmp"
SECONDARY_DST="/media/kp/AB58-B7AF/CD Backups"

EMPTY_DRIVE=0
BLANK_DISC=2048

mkdir -p "${INFO_DIR}"
mkdir -p "${IMG_DIR}"
mkdir -p "${LOG_DIR}"
mkdir -p "${TMP_DIR}"

while : 
do
	# wait until disc is ready
	echo "Please insert disc into drive."
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
			echo "Please insert disc into drive."
			eject /dev/sr0
			sleep 1
			cd_drive_size=$EMPTY_DRIVE
		else
			echo
		fi
	done

	# gather metadata and begin mirroring
	temporary_name=$(uuidgen)
	tmp_filename_prefix="${TMP_DIR}/${temporary_name}"
	echo "Mirroring to begin, writing files to '${tmp_filename_prefix}.*'"

	blkid /dev/sr0			>"${tmp_filename_prefix}.blkid.txt"
	udisksctl info --block-device /dev/sr0 \
					>"${tmp_filename_prefix}.udisks.txt"
	isoinfo -p -d -i /dev/sr0	>"${tmp_filename_prefix}.isoinfo.txt"
	ddrescue	--no-scrape \
			--sector-size=2048				\
			/dev/sr0					\
			"${tmp_filename_prefix}.img" \
			"${tmp_filename_prefix}.ddrescue.log"
	eject /dev/sr0 & # copying might take a while, so don't allow eject to block

	# request input from user
	cd_name=""
	while [[ -z "${cd_name// }" ]]
	do
		read -p "Enter text written on disc: " cd_name
	done

	mv "${tmp_filename_prefix}.blkid.txt"		"${INFO_DIR}/${cd_name}.blkid.txt"
	mv "${tmp_filename_prefix}.udisks.txt"		"${INFO_DIR}/${cd_name}.udisks.txt"
	mv "${tmp_filename_prefix}.isoinfo.txt"		"${INFO_DIR}/${cd_name}.isoinfo.txt"
	mv "${tmp_filename_prefix}.img"			"${IMG_DIR}/${cd_name}.img"
	mv "${tmp_filename_prefix}.ddrescue.log"	"${LOG_DIR}/${cd_name}.ddrescue.log"

	echo "------------------= copy files to secondary  =------------------"
	mkdir -p ~/mirror_img
	mount -o loop,ro "${IMG_DIR}/${cd_name}.img" ~/mirror_img && \
	rsync -rltzuv ~/mirror_img/ "${SECONDARY_DST}/${cd_name}" && \
	umount ~/mirror_img

	echo "------------------= done done done done done =------------------"
done
