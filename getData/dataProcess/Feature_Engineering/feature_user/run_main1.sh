nDay=1
curYear=`date -d "$nDay day ago" +"%Y"`
curMonth=`date -d "$nDay day ago" +"%m"`
curDay=`date -d "$nDay day ago" +"%d"`
Date=$curYear$curMonth$curDay
##########################################################
k=0
nohup sh run_join.sh $k $Date >> ./log/$k.log 2>&1 &
k=9
nohup sh run_join.sh $k $Date >> ./log/$k.log 2>&1 &
##########################################################
