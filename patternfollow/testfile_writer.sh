#!/bin/bash

#function ctrlc_cleanup {
#	echo "first\nfew\nlines" > $TESTFILE
#}

TESTFILE="testfile.txt"

echo "first\nfew\nlines" > $TESTFILE

echo "Start-pattern: start"
echo "End-pattern: end"
echo "Start this command within a few seconds of starting this script:"
echo "python3 filterfollow.py -f $TESTFILE -s 'start' -e 'end'"
sleep 3
while true ; do
	echo start >> $TESTFILE
	echo end >> $TESTFILE
	echo line >> $TESTFILE
	echo start >> $TESTFILE
	echo line >> $TESTFILE
	echo end >> $TESTFILE
	sleep 1
done
