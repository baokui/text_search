echo #####################################################
echo "BEGIN session feature getting in $(date "+%Y-%m-%d %H:%M:%S")"
nDay=$1
if [ ! -n "$nDay" ]; then
nDay=1
fi
curYear=`date -d "$nDay day ago" +"%Y"`
curMonth=`date -d "$nDay day ago" +"%m"`
curDay=`date -d "$nDay day ago" +"%d"`
nDayd=15
year=`date -d "$nDayd day ago" +"%Y"`
month=`date -d "$nDayd day ago" +"%m"`
day=`date -d "$nDayd day ago" +"%d"`
echo "------feature extracting - session from user_join to VpaOutput_guobk/userhistory_imagemix/feature/feature_session"
#session feature 每天都提取，每天只提取上一天的数据
sh run_main_eachday.sh $curYear $curMonth $curDay
hadoop fs -rmr VpaOutput_guobk/userhistory_imagemix/feature/feature_session/$year$month/$day/
echo "END session feature getting in $(date "+%Y-%m-%d %H:%M:%S")"