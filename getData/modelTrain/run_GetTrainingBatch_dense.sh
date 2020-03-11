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
alias mhadoop='/search/odin/software/MarsJs/bin/hadoop'
ListUser=(0 1 2 3 4 5 6 7 8 9 a b c d e f)
joining=1
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

################################################################################
echo "STEP0-mkdir files"
mkdir $resultpath
mkdir $datapath
mkdir $rootpath_user
mkdir $path_global
mkdir -p $path_user
mkdir $path_session
mkdir $path_session_test
mkdir $path_session_test_and
mkdir $path_session_test_ios
mkdir $path_userPre
mkdir -p $path_tmpdata/feature
mkdir -p log/tmp
echo "OVER-mkdir files"
################################################################################
echo "STEP1-get user and global feature"
if $DoGetData;then
#------------------------------------------------------------------------------
mhadoop fs -Dhadoop.client.ugi=$hadoopclients -ls VpaOutput_guobk/userhistory_$dataSourceuserJoin0/feature/feature_user/$Date
mhadoop fs -Dhadoop.client.ugi=$hadoopclients -ls VpaOutput_guobk/userhistory_$dataSource0/feature/feature_global/$Date
mhadoop fs -Dhadoop.client.ugi=$hadoopclients -ls VpaOutput_guobk/userhistory_$dataSourceuserJoin1/feature/feature_user/$Date
mhadoop fs -Dhadoop.client.ugi=$hadoopclients -ls VpaOutput_guobk/userhistory_$dataSource1/feature/feature_global/$Date
#------------------------------------------------------------------------------
for((u=0;u<16;u++));
do
    user=${ListUser[$u]}
    mhadoop fs -Dhadoop.client.ugi=$hadoopclients -get VpaOutput_guobk/userhistory_$dataSource0/feature/feature_global/$Date/user_$user $datapath/feature_global/user_$user-and
    mhadoop fs -Dhadoop.client.ugi=$hadoopclients -get VpaOutput_guobk/userhistory_$dataSource1/feature/feature_global/$Date/user_$user $datapath/feature_global/user_$user-ios
done
echo "GET user feature"
nbfiles=`ls $path_user| wc -w`
if [ $nbfiles -lt 32 ];then
rm -rf /search/odin/guobk/streaming/vpa/vpa-data-process/userJoinFeature/$Date/*
for((u=0;u<16;u++));
do
    user=${ListUser[$u]}
    mhadoop fs -Dhadoop.client.ugi=$hadoopclients -get VpaOutput_guobk/userhistory_$dataSourceuserJoin0/feature/feature_user/$Date/user_$user $path_user/user_$user-and
    mhadoop fs -Dhadoop.client.ugi=$hadoopclients -get VpaOutput_guobk/userhistory_$dataSourceuserJoin1/feature/feature_user/$Date/user_$user $path_user/user_$user-ios
done
else
echo "userFeature exist"
fi
sh run_userData2.sh $path_user $path_userPre
fi
echo "OVER-get user and global feature"
################################################################################
echo "STEP2-creat training batch data in tmpfile"
ListDay=''
for((i=1;i<=$nb_days;i++));
do
ListDay="$ListDay `date -d "$i day ago" +"%Y%m/%d"`"
done
ListDay=($ListDay)
for((epoch=1;epoch<4;epoch++));
do
    echo "STEP2-EPOCH-$epoch"
    for((day=0;day<$nb_days;day++));
    do
        Date_sess=${ListDay[day]}
        echo "STEP2-EPOCH-$epoch-on data $Date_sess"
        #---------------------------------------------------
        echo "STEP2-EPOCH-$epoch-on data $Date_sess-get session data"
        rm -rf /search/odin/guobk/streaming/vpa/vpa-data-process/ModelTrain-imagemix/$path_session/*
        for((u=0;u<16;u++));
        do
            user=${ListUser[$u]}
            mhadoop fs -Dhadoop.client.ugi=$hadoopclients -get VpaOutput_guobk/userhistory_$dataSource0/feature/feature_session/$Date_sess/user_$user $path_session/user_$user-and >> log/tmp/get_session.log
            mhadoop fs -Dhadoop.client.ugi=$hadoopclients -get VpaOutput_guobk/userhistory_$dataSource1/feature/feature_session/$Date_sess/user_$user $path_session/user_$user-ios >> log/tmp/get_session.log
        done
        if [ "1" -ge "$epoch" ];then
        if [ "0" -ge "$day" ];then
            mv $path_session/user_2-and  $path_session_test/
            mv $path_session/user_2-ios  $path_session_test/
            cp -r $path_session_test/user_2-and $path_session_test_and/
            cp -r $path_session_test/user_2-ios $path_session_test_ios/
        fi
        fi
        echo "OVER: STEP2-EPOCH-$epoch-on data $Date_sess-get session data"
        #---------------------------------------------------
        echo "STEP2-EPOCH-$epoch-on data $Date_sess-create tmpdata"
        platform=and
        for((u=0;u<16;u++));
        do
            user=user_${ListUser[$u]}-$platform
            python -u GetTrainingBatch_dense.py $path_global $path_user $path_session $user $path_tmpdata $epoch $Date_sess $path_userPre $joining >> ./log/tmp/tmp-$user-$epoch.log 2>&1 &
        done

        platform=ios
        for((u=0;u<15;u++));
        do
            user=user_${ListUser[$u]}-$platform
            python -u GetTrainingBatch_dense.py $path_global $path_user $path_session $user $path_tmpdata $epoch $Date_sess $path_userPre $joining >> ./log/tmp/tmp-$user-$epoch.log 2>&1 &
        done
        u=15
        user=user_${ListUser[$u]}-$platform
        python -u GetTrainingBatch_dense.py $path_global $path_user $path_session $user $path_tmpdata $epoch $Date_sess $path_userPre $joining >> ./log/tmp/tmp-$user-$epoch.log 2>&1
        #---------------------------------------------------
        nbfiles=`ls $path_session| wc -w`
        while [ $nbfiles -gt 0 ]
        do
        sleep 1
        nbfiles=`ls $path_session| wc -w`
        done
        #---------------------------------------------------
        echo "OVER: STEP2-EPOCH-$epoch-on data $Date_sess-create tmpdata"

        echo "OVER: STEP2-EPOCH-$epoch-on data $Date_sess"
    done
    echo "OVER: STEP2-EPOCH-$epoch"
done

