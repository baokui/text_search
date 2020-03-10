year=$1
month=$2
day=$3
##########################################################
for((k=0;k<10;k++));
do
    nohup sh run_join_eachday.sh $year $month $day $k >> ./log/$year-$month-$day-$k.log 2>&1 &
done
##########################################################
k=a
nohup sh run_join_eachday.sh $year $month $day $k >> ./log/$year-$month-$day-$k.log 2>&1 &
##########################################################
k=b
nohup sh run_join_eachday.sh $year $month $day $k >> ./log/$year-$month-$day-$k.log 2>&1 &
##########################################################
k=c
nohup sh run_join_eachday.sh $year $month $day $k >> ./log/$year-$month-$day-$k.log 2>&1 &
##########################################################
k=d
nohup sh run_join_eachday.sh $year $month $day $k >> ./log/$year-$month-$day-$k.log 2>&1 &
##########################################################
k=e
nohup sh run_join_eachday.sh $year $month $day $k >> ./log/$year-$month-$day-$k.log 2>&1 &
##########################################################
k=f
nohup sh run_join_eachday.sh $year $month $day $k >> ./log/$year-$month-$day-$k.log 2>&1