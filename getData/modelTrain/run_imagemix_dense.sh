echo ###update begining#################################################################
export CUDA_VISIBLE_DEVICES=3
curDate=`date -d "0 day ago" +"%Y%m%d"`
lastDate=`date -d "1 day ago" +"%Y%m%d"`
resultpath=LR$curDate-imagemix-dense
model=lr-dense
Date=$lastDate
dataSource=imagemix
DoGetData=false
DoTraining=true
echo resultpath is $resultpath
mkdir log
nohup sh run_GetTrainingBatch_dense.sh $resultpath $model $Date $dataSource $DoGetData $DoTraining >> ./log/getTmp-$Date.log 2>&1 &
nohup sh run_train_join_dense.sh $resultpath $model $Date $dataSource $DoGetData $DoTraining >> ./log/train-$Date.log 2>&1 &
nohup sh run_test_join_dense.sh $resultpath $model $Date $dataSource $DoGetData $DoTraining >> ./log/test-$Date.log 2>&1 &
echo ###update end#################################################################

