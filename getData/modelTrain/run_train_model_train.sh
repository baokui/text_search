rootpath=/search/odin/guobk/streaming/vpa/text_search/getData/modelTrain
path_global=$rootpath/data/feature_global/20200309/
path_user=$rootpath/data/feature_user/20200309/
path_session0=$rootpath/data/feature_session/202003
date=(09 08 07 06)
modelversion=model20200309
resultpath=$rootpath/$modelversion
model=lr
mkdir $resultpath
mode=train
mkdir log
for((i=0;i<${#date[@]};i++))
do
path_session=$path_session0/${date[$i]}
echo $path_session
#python -u train_model.py $mode $path_global $path_user $path_session $resultpath $model >> log/$modelversion-$mode.log
done