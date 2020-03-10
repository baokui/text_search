year=$1
month=$2
day=$3
Month=$year$month
i=$day
for((j=0;j<10;j++));
do
    nohup sh run_join.sh $j $Month $i >> ./log/$Month-$i-user_$j.log 2>&1 &
done
j=a
nohup sh run_join.sh $j $Month $i >> ./log/$Month-$i-user_$j.log 2>&1 &
j=b
nohup sh run_join.sh $j $Month $i >> ./log/$Month-$i-user_$j.log 2>&1 &
j=c
nohup sh run_join.sh $j $Month $i >> ./log/$Month-$i-user_$j.log 2>&1 &
j=d
nohup sh run_join.sh $j $Month $i >> ./log/$Month-$i-user_$j.log 2>&1 &
j=e
nohup sh run_join.sh $j $Month $i >> ./log/$Month-$i-user_$j.log 2>&1 &
j=f
nohup sh run_join.sh $j $Month $i >> ./log/$Month-$i-user_$j.log 2>&1
