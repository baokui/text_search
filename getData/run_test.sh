nDay=$1
curYear=`date -d "$nDay day ago" +"%Y"`
curMonth=`date -d "$nDay day ago" +"%m"`
curDay=`date -d "$nDay day ago" +"%d"`
curHour=`date -d "$nDay day ago" +"%H"`
for((i=0;i<1;i++));
do
    newHour=`date -d "$((24*$nDay+$curHour-$i)) hour ago" +"%H"`
    lastHour_Year=`date -d "$((24*$nDay+$curHour-$i+1)) hour ago" +"%Y"`
    lastHour_Month=`date -d "$((24*$nDay+$curHour-$i+1)) hour ago" +"%m"`
    lastHour_Day=`date -d "$((24*$nDay+$curHour-$i+1)) hour ago" +"%d"`
    lastHour_Hour=`date -d "$((24*$nDay+$curHour-$i+1)) hour ago" +"%H"`
    nextHour_Year=`date -d "$((24*$nDay+$curHour-$i-1)) hour ago" +"%Y"`
    nextHour_Month=`date -d "$((24*$nDay+$curHour-$i-1)) hour ago" +"%m"`
    nextHour_Day=`date -d "$((24*$nDay+$curHour-$i-1)) hour ago" +"%d"`
    nextHour_Hour=`date -d "$((24*$nDay+$curHour-$i-1)) hour ago" +"%H"`
    #echo $lastHour_Year$lastHour_Month$lastHour_Day$lastHour_Hour,$curYear$curMonth$curDay$newHour,$nextHour_Year$nextHour_Month$nextHour_Day$nextHour_Hour
    #done
    Year=$curYear
    Month=$curMonth
    Day=$curDay
    hour=$newHour
    input0="/cloud/dt/pingback/ping/djt-pb-log/vpapb_android_shouji/"$Year$Month"/"$Year$Month$Day"/*"$Year$Month$Day$hour"*.lzo"
    input1="/storage/sogou/desktop/imeservice/vpare/"$Year$Month"/"$Year$Month$Day"/*"$Month"-"$Day"_"$hour"*.lzo"
    logfile=./log/$Year$Month$Day/$hour.log
    Year=$lastHour_Year
    Month=$lastHour_Month
    Day=$lastHour_Day
    hour=$lastHour_Hour
    input2="/storage/sogou/desktop/imeservice/vpare/"$Year$Month"/"$Year$Month$Day"/*"$Month"-"$Day"_"$hour"*.lzo"
    Year=$nextHour_Year
    Month=$nextHour_Month
    Day=$nextHour_Day
    hour=$nextHour_Hour
    input3="/storage/sogou/desktop/imeservice/vpare/"$Year$Month"/"$Year$Month$Day"/*"$Month"-"$Day"_"$hour"*.lzo"
    nohup sh run_join.sh $input0 $input1 $input2 $input3 $curYear $curMonth $curDay $newHour>> $logfile 2>&1 &
done
