#!/usr/bin/env bash

echo -n "Enter CD name and press [ENTER]: "

while read cd_name
do
	# check if nothing was input
	if [[ -z "${cd_name// }" ]]
	then
		exit
	fi

	echo "================================================================"
	echo "Reading CD '${cd_name}'"
	#isoinfo -p -d -i /dev/cdrom >"${cd_name}.isoinfo.txt"
	#ddrescue -n -b 2048 /dev/cdrom "${cd_name}.iso" "${cd_name}.log"

	echo "------------------= done done done done done =------------------"
	echo -n "Enter CD name and press [ENTER]: "
done < "${1:-/dev/stdin}"
