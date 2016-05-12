#!/usr/bin/env bash
alias hfs='/usr/bin/hadoop fs '
export HAS=/opt/cloudera/parcels/CDH­5.4.5­1.cdh5.4.5.p0.7/jars export HSJ=hadoop­streaming­2.6.0­cdh5.4.5.jar
alias hjs='/usr/bin/hadoop jar $HAS/$HSJ'


#upload data
hfs -mkdir yellow_input
hfs -put ./data/yellow_tripdata_2015-*.csv /user/mw3265/yellow_input/

#upload data
hfs -mkdir green_input
hfs -put ./data/green_tripdata_2015-*.csv /user/mw3265/green_input/

# stats
cd preprocess
hfs -rm -r /user/mw3265/YellowResult
hjs -D mapreduce.job.reduces=4 -files map.py,reduce.py -mapper map.py -reducer reduce.py -input /user/mw3265/yellow_input/yellow_tripdata_2015-01.csv -input /user/mw3265/yellow_input/yellow_tripdata_2015-02.csv -input /user/mw3265/yellow_input/yellow_tripdata_2015-03.csv -input /user/mw3265/yellow_input/yellow_tripdata_2015-04.csv -input /user/mw3265/yellow_input/yellow_tripdata_2015-05.csv -input /user/mw3265/yellow_input/yellow_tripdata_2015-06.csv -input /user/mw3265/yellow_input/yellow_tripdata_2015-07.csv -input /user/mw3265/yellow_input/yellow_tripdata_2015-08.csv -input /user/mw3265/yellow_input/yellow_tripdata_2015-09.csv -input /user/mw3265/yellow_input/yellow_tripdata_2015-10.csv -input /user/mw3265/yellow_input/yellow_tripdata_2015-11.csv -input /user/mw3265/yellow_input/yellow_tripdata_2015-12.csv -output /user/mw3265/YellowResult
hfs -get /user/mw3265/YellowResult
cd ..

# stats
cd preprocess
hfs -rm -r /user/mw3265/GreenResult
hjs -D mapreduce.job.reduces=2 -files map.py,reduce.py -mapper map.py -reducer reduce.py -input /user/mw3265/green_input/green_tripdata_2015-01.csv -input /user/mw3265/green_input/green_tripdata_2015-02.csv -input /user/mw3265/green_input/green_tripdata_2015-03.csv -input /user/mw3265/green_input/green_tripdata_2015-04.csv -input /user/mw3265/green_input/green_tripdata_2015-05.csv -input /user/mw3265/green_input/green_tripdata_2015-06.csv -input /user/mw3265/green_input/green_tripdata_2015-07.csv -input /user/mw3265/green_input/green_tripdata_2015-08.csv -input /user/mw3265/green_input/green_tripdata_2015-09.csv -input /user/mw3265/green_input/green_tripdata_2015-10.csv -input /user/mw3265/green_input/green_tripdata_2015-11.csv -input /user/mw3265/green_input/green_tripdata_2015-12.csv -output /user/mw3265/GreenResult
hfs -get /user/mw3265/GreenResult
cd ..

cd polygon
# preprocess polygon data
INS="`seq -w 1 12`"
for f in ${INS}; do
    time python parse_polygon.py ../../data/green_tripdata_2015-${f}.csv > ../../data/green_2015_${f}_poly.txt
done
for f in ${INS}; do
    time python parse_polygon.py ../../data/yellow_tripdata_2015-${f}.csv > ../../data/yellow_2015_${f}_poly.txt
done
cd ..

#upload data
hfs -mkdir yellow_input
hfs -put ./data/yellow_2015_*.txt /user/mw3265/yellow_input/

#upload data
hfs -mkdir green_input
hfs -put ../data/green_2015_*.txt /user/mw3265/green_input/

# polygon stats
cd polygon
hfs -rm -r /user/mw3265/YellowPolygonResult
hjs -D mapreduce.job.reduces=1 -files map2.py,reduce.py -mapper map2.py -reducer reduce.py -input /user/mw3265/yellow_input/yellow_2015_01_poly.txt -input /user/mw3265/yellow_input/yellow_2015_02_poly.txt -input /user/mw3265/yellow_input/yellow_2015_03_poly.txt -input /user/mw3265/yellow_input/yellow_2015_04_poly.txt -input /user/mw3265/yellow_input/yellow_2015_05_poly.txt -input /user/mw3265/yellow_input/yellow_2015_06_poly.txt -input /user/mw3265/yellow_input/yellow_2015_07_poly.txt -input /user/mw3265/yellow_input/yellow_2015_08_poly.txt -input /user/mw3265/yellow_input/yellow_2015_09_poly.txt -input /user/mw3265/yellow_input/yellow_2015_10_poly.txt -input /user/mw3265/yellow_input/yellow_2015_11_poly.txt -input /user/mw3265/yellow_input/yellow_2015_12_poly.txt -output /user/mw3265/YellowPolygonResult
hfs -get /user/mw3265/YellowPolygonResult
cd ..

cd polygon
hfs -rm -r /user/mw3265/GreenPolygonResult
hjs -D mapreduce.job.reduces=1 -files map2.py,reduce.py -mapper map2.py -reducer reduce.py -input /user/mw3265/green_input/green_2015_01_poly.txt -input /user/mw3265/green_input/green_2015_02_poly.txt -input /user/mw3265/green_input/green_2015_03_poly.txt -input /user/mw3265/green_input/green_2015_04_poly.txt -input /user/mw3265/green_input/green_2015_05_poly.txt -input /user/mw3265/green_input/green_2015_06_poly.txt -input /user/mw3265/green_input/green_2015_07_poly.txt -input /user/mw3265/green_input/green_2015_08_poly.txt -input /user/mw3265/green_input/green_2015_09_poly.txt -input /user/mw3265/green_input/green_2015_10_poly.txt -input /user/mw3265/green_input/green_2015_11_poly.txt -input /user/mw3265/green_input/green_2015_12_poly.txt -output /user/mw3265/GreenPolygonResult
hfs -get /user/mw3265/GreenPolygonResult
cd ..

# neighourhood trips stats

cd polygon
hfs -rm -r /user/mw3265/YellowNghTripStats
hjs -D mapreduce.job.reduces=4 -files map2.py,reduce2.py -mapper map2.py -reducer reduce2.py -input /user/mw3265/yellow_input/yellow_2015_01_poly.txt -input /user/mw3265/yellow_input/yellow_2015_02_poly.txt -input /user/mw3265/yellow_input/yellow_2015_03_poly.txt -input /user/mw3265/yellow_input/yellow_2015_04_poly.txt -input /user/mw3265/yellow_input/yellow_2015_05_poly.txt -input /user/mw3265/yellow_input/yellow_2015_06_poly.txt -input /user/mw3265/yellow_input/yellow_2015_07_poly.txt -input /user/mw3265/yellow_input/yellow_2015_08_poly.txt -input /user/mw3265/yellow_input/yellow_2015_09_poly.txt -input /user/mw3265/yellow_input/yellow_2015_10_poly.txt -input /user/mw3265/yellow_input/yellow_2015_11_poly.txt -input /user/mw3265/yellow_input/yellow_2015_12_poly.txt -output /user/mw3265/YellowNghTripStats
#hfs -get /user/mw3265/YellowNghTripStats
cd ..

cd polygon
hfs -rm -r /user/mw3265/GreenNghTripStats
hjs -D mapreduce.job.reduces=4 -files map2.py,reduce2.py -mapper map2.py -reducer reduce2.py -input /user/mw3265/green_input/green_2015_01_poly.txt -input /user/mw3265/green_input/green_2015_02_poly.txt -input /user/mw3265/green_input/green_2015_03_poly.txt -input /user/mw3265/green_input/green_2015_04_poly.txt -input /user/mw3265/green_input/green_2015_05_poly.txt -input /user/mw3265/green_input/green_2015_06_poly.txt -input /user/mw3265/green_input/green_2015_07_poly.txt -input /user/mw3265/green_input/green_2015_08_poly.txt -input /user/mw3265/green_input/green_2015_09_poly.txt -input /user/mw3265/green_input/green_2015_10_poly.txt -input /user/mw3265/green_input/green_2015_11_poly.txt -input /user/mw3265/green_input/green_2015_12_poly.txt -output /user/mw3265/GreenNghTripStats
#hfs -get /user/mw3265/GreenNghTripStats
cd ..

cd polygon
hfs -rm -r /user/mw3265/YellowNghTripStatsMerge
hjs -D mapreduce.job.reduces=1 -files map2.py,reduce3.py -mapper map2.py -reducer reduce3.py -input /user/mw3265/YellowNghTripStats -output /user/mw3265/YellowNghTripStatsMerge
hfs -get /user/mw3265/YellowNghTripStatsMerge
cd ..

cd polygon
hfs -rm -r /user/mw3265/GreenNghTripStatsMerge
hjs -D mapreduce.job.reduces=1 -files map2.py,reduce3.py -mapper map2.py -reducer reduce3.py -input /user/mw3265/GreenNghTripStats -output /user/mw3265/GreenNghTripStatsMerge
hfs -get /user/mw3265/GreenNghTripStatsMerge
cd ..