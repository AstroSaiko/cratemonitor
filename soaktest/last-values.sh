#!/bin/bash
# This script will get the last data 

rrdtool lastupdate ./rrd/mch-s1g04-18.rrd > last-rrd-values.dat
rrdtool lastupdate ./rrd/mch-s1g04-27.rrd >> last-rrd-values.dat
rrdtool lastupdate ./rrd/mch-s1g04-36.rrd > last-rrd-values.dat
rrdtool lastupdate ./rrd/mch-s1g04-45.rrd >> last-rrd-values.dat
#rrdtool lastupdate s1e03-18.rrd >> last-rrd-values.dat
#rrdtool lastupdate s1e02-27.rrd >> last-rrd-values.dat
#rrdtool lastupdate s1e02-18.rrd >> last-rrd-values.dat
#rrdtool lastupdate s1e02-10.rrd >> last-rrd-values.dat
