rootpath=/search/odin/guobk/streaming/vpa/vpa-data-process/logdata-process/get_alldata
echo ------------------------------------------------------------------------------------------------
echo "BEGIN imagemix data update in $(date "+%Y-%m-%d %H:%M:%S")"
nDay=1
curYear=`date -d "$nDay day ago" +"%Y"`
curMonth=`date -d "$nDay day ago" +"%m"`
curDay=`date -d "$nDay day ago" +"%d"`
Time=$curYear$curMonth$curDay
######################################################################################################

#############global feature##############################################################################
echo "------feature extracting - global from user_join to VpaOutput_guobk/userhistory_imagemix/feature/feature_global"
cd $rootpath/LRmodel-imagemix/dataProcess/Feature_Engineering/feature_global
sh run_main.sh

#############user feature#############################################################################
echo "------feature extracting - user from user_join to VpaOutput_guobk/userhistory_imagemix/feature/feature_user"
cd $rootpath/LRmodel-imagemix/dataProcess/Feature_Engineering/feature_user
sh run_main.sh
#############session feature#############################################################################
echo "------feature extracting - session from user_join to VpaOutput_guobk/userhistory_imagemix/feature/feature_user"
cd $rootpath/LRmodel-imagemix/dataProcess/Feature_Engineering/feature_session
sh run_sess_lastday.sh 1
##############data delete###############################################################################
nDay=10
curYear=`date -d "$nDay day ago" +"%Y"`
curMonth=`date -d "$nDay day ago" +"%m"`
curDay=`date -d "$nDay day ago" +"%d"`
Date=$curYear$curMonth$curDay
hadoop fs -rmr VpaOutput_guobk/userhistory_imagemix/user_join/$Date
hadoop fs -rmr VpaOutput_guobk/userhistory_imagemix/feature/feature_user/$Date
hadoop fs -rmr VpaOutput_guobk/userhistory_imagemix/feature/feature_global/$Date
#############################################################################

echo "END imagemix data update in $(date "+%Y-%m-%d %H:%M:%S")"
echo ------------------------------------------------------------------------------------------------