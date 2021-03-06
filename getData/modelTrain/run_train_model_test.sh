rootpath=/search/odin/guobk/streaming/vpa/text_search/getData/modelTrain
path_global=$rootpath/data/feature_global/20200309/
path_user=$rootpath/data/feature_user/20200309/
path_session=$rootpath/data/TEST
modelversion=model20200309
resultpath=$rootpath/$modelversion
model=lr
mode=test
for((i=0;i<1000;i++))
do
python -u train_model.py $mode $path_global $path_user $path_session $resultpath $model >> log/$modelversion-$mode.log
done