#!/usr/bin/env bash
while read cd_name
do
  echo "${cd_name}"
done < "${1:-/dev/stdin}"
