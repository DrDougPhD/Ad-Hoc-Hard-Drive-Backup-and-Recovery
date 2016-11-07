#!/usr/bin/env bash
#
# TODO
#	Continuously loop until disc is inserted and ready
#	Detect when blank disc is inserted and notify user
#	When image has been duplicated, mount image and copy files to secondary
#		location.
#
USER_PROMPT="Enter CD name and press [ENTER]: "
INFO_DIR="info"
IMG_DIR="img"
LOG_DIR="log"

mkdir -p "${INFO_DIR}"
mkdir -p "${IMG_DIR}"
mkdir -p "${LOG_DIR}"

echo -n "${USER_PROMPT} "

while read cd_name
do
	# check if nothing was input
	if [[ -z "${cd_name// }" ]]
	then
		exit
	fi

	echo "================================================================"
	echo "Reading CD '${cd_name}'"
	blkid /dev/sr0			>"${INFO_DIR}/${cd_name}.blkid.txt"
	isoinfo -p -d -i /dev/sr0	>"${INFO_DIR}/${cd_name}.isoinfo.txt"
	ddrescue	--no-scrape \
			--sector-size=2048 \
			/dev/sr0					\
			"${IMG_DIR}/${cd_name}.img" \
			"${LOG_DIR}/${cd_name}.ddrescue.log"
	eject /dev/sr0

	echo "------------------= done done done done done =------------------"
	echo -n "${USER_PROMPT} "
done < "${1:-/dev/stdin}"
