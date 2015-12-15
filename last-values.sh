#!/bin/bash
# This script will get the last data 

rrdtool lastupdate mch01.rrd > last-rrd-values.dat
rrdtool lastupdate mch02.rrd >> last-rrd-values.dat
#rrdtool lastupdate s1e03-18.rrd >> last-rrd-values.dat
#rrdtool lastupdate s1e02-27.rrd >> last-rrd-values.dat
#rrdtool lastupdate s1e02-18.rrd >> last-rrd-values.dat
#rrdtool lastupdate s1e02-10.rrd >> last-rrd-values.dat
