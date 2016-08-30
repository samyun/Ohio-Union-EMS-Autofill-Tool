#!/bin/bash
# Script to install requirements for the Ohio Union EMS Autofill Tool. This
# script only runs on Mac (tested against OS X 10.11.6 El Capitan). If you're
# on a different platform (Windows/Linux), see README for manual installation.

clear
echo "Enter location to put files (default ~/EMSAutofill): "
read LOCATION

if [ ${#LOCATION} -eq 0 ]; then
    LOCATION="$HOME/EMSAutofill"
fi

if [ ! -d "$LOCATION" ]; then
    mkdir $LOCATION
fi

cd $LOCATION

echo $PWD
