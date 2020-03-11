resultpath=$1
model=$2
Date=$3
dataSource=$4
DoGetData=$5
DoTraining=$6
hadoopclients=ml_research,3evrqV2R
nb_days=7
join=1
dataSource0=$dataSource
dataSource1=${dataSource}_ios
dataSourceuserJoin0=userFeatureJoin
dataSourceuserJoin1=userFeatureJoin_ios
rootpath_user=/search/odin/guobk/streaming/vpa/vpa-data-process/userJoinFeature
ListUser=(0 1 2 3 4 5 6 7 8 9 a b c d e f)
##############################################################################
datapath=$resultpath/data
path_global=$datapath/feature_global
path_user=$rootpath_user/$Date
path_session=$datapath/feature_session
path_session_test=$datapath/TEST
path_session_test_and=$datapath/TEST-and
path_session_test_ios=$datapath/TEST-ios
path_userPre=$datapath/userPre
path_tmpdata=$resultpath/tmpdata
#########################################################################################
#---------------------------------------------------------------------------------------
for((i=0;i<10000;i++));
do
echo ---------------------------------------
echo test for $i times
python -u train_model.py predict $model $path_global $path_user $path_session $path_session_test $resultpath $path_userPre $join
echo ---------------------------------------
done