#!/usr/bin/env bash
ROOT="$2"
while read URL; do
	if [ ! -z "${URL// }" ]
	then	# the current URL is not empty
		ABSPATH="${ROOT}${URL}"
		if [ -e "$ABSPATH" ]
		then	# file exists where it should
			echo "Checking if file exists..."
			if [ -e ./"$( basename '${URL}' )" ]
			then	# there exists a file here with that name
				echo "DUPLICATE FILE"
			else
				ln -s "${ROOT}${URL}" ./
			fi
		else
			echo "Source file doesn't exist:" ${ABSPATH}
		fi
	fi
done < $1

