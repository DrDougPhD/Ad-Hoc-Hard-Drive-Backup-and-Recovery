#!/usr/bin/env bash
#
# TODO
#	Detect if inserted disc is a music CD
#	If user cancels, ask if they want to delete temporary files
#	Pretty console output stuff, like centering and box symbols and shit
#	Prefix final name of disc by a timestamp obtained from within the disc,
#		useful in determining how old the disc is and what kind of
#		files may reside on it.
#	Also, do the files have any usernames associated to them?
#	For unmarked discs, prepend their current number to the beginning of
#		their image file name
#	Test that the user is permitted to create files, dirs, whatever for
#		this script
#	Make temporary name based on disc info so that, if prematurely
#		cancelled, it can resume from where it stopped
#
INFO_DIR="info"
IMG_DIR="img"
LOG_DIR="mapfiles"
TMP_DIR=".tmp"
MNT_DIR="file_access"
TMP_MOUNT_DIR="${TMP_DIR}/mnt"
SECONDARY_DST="/media/kp/AB58-B7AF/CD Backups" #TODO: make general?
FUTURE_MOUNTING_SCRIPT="${MNT_DIR}/mount_disc_images.sh"

# constants assisting in detecting if the drive is open or not ready, or if
# the disc is empty.
EMPTY_DRIVE=0
BLANK_DISC=2048

mkdir -p "${INFO_DIR}"
mkdir -p "${IMG_DIR}"
mkdir -p "${LOG_DIR}"
mkdir -p "${TMP_DIR}"
mkdir -p "${MNT_DIR}"
mkdir -p "${TMP_MOUNT_DIR}"

while : 
do
	# wait until disc is ready
	echo "Please insert disc into drive."
	disc_bytesize=$EMPTY_DRIVE
	while [[ $disc_bytesize -le $BLANK_DISC ]]
	do
		echo -ne "."
		disc_bytesize=$(udisksctl info --block-device /dev/sr0 | grep 'Size:' | awk -F' ' '{ print $2 }' -)
		if	[[ $disc_bytesize -eq $EMPTY_DRIVE ]]
		then	# disc tray is still open, or has not spun up yet
			sleep 1
		elif	[[ $disc_bytesize -eq $BLANK_DISC  ]]
		then	# a blank disc has been inserted, eject it and start again
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
	tmp_path="${TMP_DIR}/${temporary_name}"
	mkdir -p "${tmp_path}"
	echo "Inserted disc is $(numfmt --to=si --suffix=B --format='%1f' ${disc_bytesize}) long!" #TODO: wrap to next line
	echo "Mirroring to begin, writing files into '${tmp_path}/'"

	blkid /dev/sr0			>"${tmp_path}/blkid.txt"
	udisksctl info --block-device /dev/sr0 \
					>"${tmp_path}/udisks.txt"
	isoinfo -p -d -i /dev/sr0	>"${tmp_path}/isoinfo.txt" #TODO: will not work on DVDs, which use UDF I think.
	ddrescue	--no-scrape \
			--sector-size=2048				\
			/dev/sr0					\
			"${tmp_path}/img"				\
			"${tmp_path}/ddrescue.map"

	# test if anything was salvaged from disc
	if [[ ! -s "${tmp_path}/img" ]]
	then
		echo "Nothing recovered from disc. Deleting files. Moving on to next disc."
		echo "Store disc for later recovery efforts / trial on another CD drive."
		rm -R "${tmp_path}"
		echo "--------------------------------------------------------"
		eject /dev/sr0
	else
		echo "------------------= copy files to secondary  =------------------"
		# the image might be faulty, so mounting might fail
		# don't do the other commands if it is faulty
		#TODO: rsync might fail, which would prevent this stuff from happeneing...
		mount -o loop,ro "${tmp_path}/img" "${TMP_MOUNT_DIR}" && \
		rsync -rltzuv "${TMP_MOUNT_DIR}/" "${SECONDARY_DST}/${temporary_name}" && \
		umount "${TMP_MOUNT_DIR}"

		# request input from user
		echo "Transfer complete!"
		eject /dev/sr0 & # open the drive, but don't block rest of program
		cd_name=""
		while [[ -z "${cd_name// }" ]]
		do
			read -p "Enter text written on disc: " cd_name
		done

		# TODO perhaps there's a cleaner way to do this
		mv "${tmp_path}/blkid.txt"	"${INFO_DIR}/${cd_name}.blkid.txt"
		mv "${tmp_path}/udisks.txt"	"${INFO_DIR}/${cd_name}.udisks.txt"
		mv "${tmp_path}/isoinfo.txt"	"${INFO_DIR}/${cd_name}.isoinfo.txt"
		mv "${tmp_path}/img"		"${IMG_DIR}/${cd_name}.img"
		mv "${tmp_path}/ddrescue.map"	"${LOG_DIR}/${cd_name}.ddrescue.map"

		# to aid in future exploring of files on these images, add their
		# info to a script
		mount_point="${MNT_DIR}/${cd_name}"
		echo "mkdir -p '${mount_point}'"					>>"${FUTURE_MOUNTING_SCRIPT}"
		echo "mount -o loop,ro '${IMG_DIR}/${cd_name}.img' '${mount_point}'"	>>"${FUTURE_MOUNTING_SCRIPT}"

		# secondary storage files are still under the uuid directory
		# move these to a directory with the provided name
		mv "${SECONDARY_DST}/${temporary_name}" "${SECONDARY_DST}/${cd_name}"

		echo "------------------= done done done done done =------------------"
	fi
done
