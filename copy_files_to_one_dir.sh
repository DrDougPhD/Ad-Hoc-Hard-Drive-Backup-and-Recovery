#!/usr/bin/env bash
ROOT="$2"
while read URL; do
	#FILENAME=$( /usr/bin/basename "$PATH" )
	#echo -e "$FILENAME \t $PATH" 
	if [ ! -z "${URL// }" ]
	then
		ln -s "${ROOT}${URL}" ./
		#if [ -e $(basename "${URL}") ]
		#then
		#	echo "DUPLICATE FILE"
		#else
		#fi
	fi
done < $1

