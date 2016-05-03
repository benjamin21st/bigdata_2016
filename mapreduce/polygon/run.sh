#!/bin/bash

INS="`seq -w 1 12`"  
for f in ${INS}; do
    time python parse_polygon.py ../../data/green_tripdata_2015-${f}.csv > ../../data/green_2015_${f}_poly.txt
done
for f in ${INS}; do
    time python parse_polygon.py ../../data/yellow_tripdata_2015--${f}.csv > ../../data/yellow_2015_${f}_poly.txt
done
    