#under data
#hfs -mkdir yellow_input
#hfs -put yellow_tripdata_2015-*.csv /user/mw3265/yellow_input/

#under data
#hfs -mkdir green_input
#hfs -put green_tripdata_2015-*.csv /user/mw3265/green_input/

cd preprocess
hfs -rm -r /user/mw3265/YellowResult
hjs -D mapreduce.job.reduces=4 -files map.py,reduce.py -mapper map.py -reducer reduce.py -input /user/mw3265/yellow_input/yellow_tripdata_2015-01.csv -input /user/mw3265/yellow_input/yellow_tripdata_2015-02.csv -input /user/mw3265/yellow_input/yellow_tripdata_2015-03.csv -input /user/mw3265/yellow_input/yellow_tripdata_2015-04.csv -input /user/mw3265/yellow_input/yellow_tripdata_2015-05.csv -input /user/mw3265/yellow_input/yellow_tripdata_2015-06.csv -input /user/mw3265/yellow_input/yellow_tripdata_2015-07.csv -input /user/mw3265/yellow_input/yellow_tripdata_2015-08.csv -input /user/mw3265/yellow_input/yellow_tripdata_2015-09.csv -input /user/mw3265/yellow_input/yellow_tripdata_2015-10.csv -input /user/mw3265/yellow_input/yellow_tripdata_2015-11.csv -input /user/mw3265/yellow_input/yellow_tripdata_2015-12.csv -output /user/mw3265/YellowResult
hfs -get /user/mw3265/YellowResult
cd ..

cd preprocess
hfs -rm -r /user/mw3265/GreenResult
hjs -D mapreduce.job.reduces=2 -files map.py,reduce.py -mapper map.py -reducer reduce.py -input /user/mw3265/green_input/green_tripdata_2015-01.csv -input /user/mw3265/green_input/green_tripdata_2015-02.csv -input /user/mw3265/green_input/green_tripdata_2015-03.csv -input /user/mw3265/green_input/green_tripdata_2015-04.csv -input /user/mw3265/green_input/green_tripdata_2015-05.csv -input /user/mw3265/green_input/green_tripdata_2015-06.csv -input /user/mw3265/green_input/green_tripdata_2015-07.csv -input /user/mw3265/green_input/green_tripdata_2015-08.csv -input /user/mw3265/green_input/green_tripdata_2015-09.csv -input /user/mw3265/green_input/green_tripdata_2015-10.csv -input /user/mw3265/green_input/green_tripdata_2015-11.csv -input /user/mw3265/green_input/green_tripdata_2015-12.csv -output /user/mw3265/GreenResult
hfs -get /user/mw3265/GreenResult
cd ..