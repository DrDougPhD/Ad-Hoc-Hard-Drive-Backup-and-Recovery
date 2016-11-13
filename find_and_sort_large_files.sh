#!/usr/bin/env bash
#
# Build a list of all files stored (recursively) within a specified directory
# such that the list is sorted in descending order by each file's size.
#
DIRECTORY="$1"
if [ -z "$DIRECTORY" ]
then
	DIRECTORY='./'
fi

find "$DIRECTORY" -type f -printf "%s\t${DIRECTORY}%P\n"                       \
| sort --numeric-sort --key=1 --reverse --parallel=4                           \
| numfmt --to=si --field=1 --suffix=B --format="%.1f"                          \
| gzip -c - >2016-11-13.big_files.txt.gz
#       -h, --human-numeric-sort
#              compare human readable numbers (e.g., 2K 1G)
#       -n, --numeric-sort
#              compare according to string numerical value
#       --compress-program=PROG
#              compress temporaries with PROG; decompress them with PROG -d
#       -k, --key=KEYDEF
#              sort via a key; KEYDEF gives location and type
#       --parallel=N
#              change the number of sorts run concurrently to N
#       -r, --reverse
#              reverse the result of comparisons
#       -t, --field-separator=SEP
#              use SEP instead of non-blank to blank transition
#       KEYDEF  is  F[.C][OPTS][,F[.C][OPTS]] for start and stop position, where F is a field number and C a character position in the field; both are origin 1, and the stop position defaults to the line's
#       end.  If neither -t nor -b is in effect, characters in a field are counted from the beginning of the preceding whitespace.  OPTS is one or more single-letter ordering options  [bdfgiMhnRrV],  which
#       override global ordering options for that key.  If no key is given, use the entire line as the key.  Use --debug to diagnose incorrect key usage.








