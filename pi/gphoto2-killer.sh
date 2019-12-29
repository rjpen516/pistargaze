#!/bin/bash

while true
do
	for PID in `ps aux | grep -e gvfs.*gphoto2 | grep -v grep | awk '{print $2}'`
	do
		echo "killing $PID"
		kill -9 $PID
	done

	sleep 10
done
