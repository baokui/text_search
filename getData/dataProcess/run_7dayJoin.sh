rootpath=/search/odin/guobk/streaming/vpa/text_search/getData
echo ------------------------------------------------------------------------------------------------
echo "BEGIN imagemix data update in $(date "+%Y-%m-%d %H:%M:%S")"
nDay=1
curYear=`date -d "$nDay day ago" +"%Y"`
curMonth=`date -d "$nDay day ago" +"%m"`
curDay=`date -d "$nDay day ago" +"%d"`
Time=$curYear$curMonth$curDay
######################################################################################################
############join 7days data###########################################################################
# 用户7天历史点击的join
echo "------join 7 days data from VpaOutput_guobk/userhistory_godText/user_*/ to VpaOutput_guobk/userhistory_godText/user_join/"
cd $rootpath/dataProcess/History_Join
sh run_main.sh >> ./log/merge_$Time.log 2>&1
