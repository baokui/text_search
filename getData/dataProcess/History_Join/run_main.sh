beforeday=4
nDay=1
curYear=`date -d "$nDay day ago" +"%Y"`
curMonth=`date -d "$nDay day ago" +"%m"`
curDay=`date -d "$nDay day ago" +"%d"`
Date=$curYear$curMonth$curDay
##########################################################
for((j=0;j<10;j++));
do
    file_from=''
    for((i=1;i<=$beforeday;i++));
    do
    file_from="$file_from VpaOutput_guobk/userhistory_godText/user_$j/`date -d "$i day ago" +"%Y%m/%d"`/part*"
    done
    nohup sh run_join.sh $j $file_from $Date >> ./log/user_$j.log 2>&1 &
done
##################################################
j=a
file_from=''
for((i=1;i<=$beforeday;i++));
do
file_from="$file_from VpaOutput_guobk/userhistory_godText/user_$j/`date -d "$i day ago" +"%Y%m/%d"`/part*"
done
nohup sh run_join.sh $j $file_from $Date >> ./log/user_$j.log 2>&1 &
###########################################################
j=b
file_from=''
for((i=1;i<=$beforeday;i++));
do
file_from="$file_from VpaOutput_guobk/userhistory_godText/user_$j/`date -d "$i day ago" +"%Y%m/%d"`/part*"
done
nohup sh run_join.sh $j $file_from $Date >> ./log/user_$j.log 2>&1 &
###########################################################
j=c
file_from=''
for((i=1;i<=$beforeday;i++));
do
file_from="$file_from VpaOutput_guobk/userhistory_godText/user_$j/`date -d "$i day ago" +"%Y%m/%d"`/part*"
done
nohup sh run_join.sh $j $file_from $Date >> ./log/user_$j.log 2>&1 &
###########################################################
j=d
file_from=''
for((i=1;i<=$beforeday;i++));
do
file_from="$file_from VpaOutput_guobk/userhistory_godText/user_$j/`date -d "$i day ago" +"%Y%m/%d"`/part*"
done
nohup sh run_join.sh $j $file_from $Date >> ./log/user_$j.log 2>&1 &
###########################################################
j=e
file_from=''
for((i=1;i<=$beforeday;i++));
do
file_from="$file_from VpaOutput_guobk/userhistory_godText/user_$j/`date -d "$i day ago" +"%Y%m/%d"`/part*"
done
nohup sh run_join.sh $j $file_from $Date >> ./log/user_$j.log 2>&1 &
###########################################################
j=f
file_from=''
for((i=1;i<=$beforeday;i++));
do
file_from="$file_from VpaOutput_guobk/userhistory_godText/user_$j/`date -d "$i day ago" +"%Y%m/%d"`/part*"
done
nohup sh run_join.sh $j $file_from $Date >> ./log/user_$j.log 2>&1
###########################################################