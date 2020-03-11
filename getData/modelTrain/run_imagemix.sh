echo ###update begining#################################################################
export CUDA_VISIBLE_DEVICES=3
curDate=`date -d "0 day ago" +"%Y%m%d"`
lastDate=`date -d "1 day ago" +"%Y%m%d"`
ps -ef|grep LR$lastDate-imagemix|grep -v grep|awk  '{print "kill -9 " $2}' |sh
resultpath=LR$curDate-imagemix
model=lr
Date=$lastDate
dataSource=imagemix
DoGetData=true
DoTraining=true
DoGetUserFeature=false
echo resultpath is $resultpath
mkdir log
nohup sh run_GetTrainingBatch.sh $resultpath $model $Date $dataSource $DoGetData $DoTraining $DoGetUserFeature >> ./log/getTmp-$Date.log 2>&1 &
nohup sh run_train_join.sh $resultpath $model $Date $dataSource $DoGetData $DoTraining >> ./log/train-$Date.log 2>&1 &
nohup sh run_test_join.sh $resultpath $model $Date $dataSource $DoGetData $DoTraining >> ./log/test-$Date.log 2>&1 &
echo ###update end#################################################################

