nDay=$1
curYear=`date -d "$nDay day ago" +"%Y"`
curMonth=`date -d "$nDay day ago" +"%m"`
curDay=`date -d "$nDay day ago" +"%d"`
curHour=`date -d "$nDay day ago" +"%H"`
if [ ! -d "./log/$curYear$curMonth$curDay" ];then
mkdir ./log/$curYear$curMonth$curDay
fi
sh run_0_8.sh $nDay
sh run_8_16.sh $nDay
sh run_16_24.sh $nDay



