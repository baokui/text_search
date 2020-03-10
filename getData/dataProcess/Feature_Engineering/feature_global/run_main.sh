##########################################################
nDay=1
curYear=`date -d "$nDay day ago" +"%Y"`
curMonth=`date -d "$nDay day ago" +"%m"`
curDay=`date -d "$nDay day ago" +"%d"`
Date=$curYear$curMonth$curDay
nohup sh run_join.sh 0 $Date >> ./log/0.log 2>&1 &
nohup sh run_join.sh 1 $Date >> ./log/1.log 2>&1 &
nohup sh run_join.sh 2 $Date >> ./log/2.log 2>&1 &
nohup sh run_join.sh 3 $Date >> ./log/3.log 2>&1 &
nohup sh run_join.sh 4 $Date >> ./log/4.log 2>&1 &
nohup sh run_join.sh 5 $Date >> ./log/5.log 2>&1 &
nohup sh run_join.sh 6 $Date >> ./log/6.log 2>&1 &
nohup sh run_join.sh 7 $Date >> ./log/7.log 2>&1 &
nohup sh run_join.sh 8 $Date >> ./log/8.log 2>&1 &
nohup sh run_join.sh 9 $Date >> ./log/9.log 2>&1 &
nohup sh run_join.sh a $Date >> ./log/a.log 2>&1 &
nohup sh run_join.sh b $Date >> ./log/b.log 2>&1 &
nohup sh run_join.sh c $Date >> ./log/c.log 2>&1 &
nohup sh run_join.sh d $Date >> ./log/d.log 2>&1 &
nohup sh run_join.sh e $Date >> ./log/e.log 2>&1 &
nohup sh run_join.sh f $Date >> ./log/f.log 2>&1
##########################################################
