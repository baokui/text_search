nDay=$1
curYear=`date -d "$nDay day ago" +"%Y"`
curMonth=`date -d "$nDay day ago" +"%m"`
curDay=`date -d "$nDay day ago" +"%d"`
Date=$curYear$curMonth$curDay
##########################################################
for((k=0;k<7;k++));
do
    nohup sh run_join.sh $k $Date >> ./log/$k.log 2>&1 &
done
k=7
nohup sh run_join.sh $k $Date >> ./log/$k.log 2>&1 &
##########################################################
k=8
nohup sh run_join.sh $k $Date >> ./log/$k.log 2>&1 &
k=9
nohup sh run_join.sh $k $Date >> ./log/$k.log 2>&1 &
k=a
nohup sh run_join.sh $k $Date >> ./log/$k.log 2>&1 &
k=b
nohup sh run_join.sh $k $Date >> ./log/$k.log 2>&1 &
k=c
nohup sh run_join.sh $k $Date >> ./log/$k.log 2>&1 &
k=d
nohup sh run_join.sh $k $Date >> ./log/$k.log 2>&1 &
k=e
nohup sh run_join.sh $k $Date >> ./log/$k.log 2>&1 &
k=f
nohup sh run_join.sh $k $Date >> ./log/$k.log 2>&1