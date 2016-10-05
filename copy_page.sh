#!/bin/bash

echo 'Copying files for webpage!'
export DIRNAME="/afs/cern.ch/user/g/gauzinge/www/cratemonitor/"
echo 'moving files to' $DIRNAME
cp /home/xtaldaq/cratemonitor/*.png $DIRNAME
