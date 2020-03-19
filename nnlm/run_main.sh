path_source=zhangfeixue/nlg/userdata/
path_target=VpaOutput_guobk/dabaigou_train_nnlm/
for((idx=0;idx<10;idx++))
do
input=$path_source/part-0$idx*
output=$path_target/00$idx
nohup sh run_join.sh $input $output >> log/00$idx.log 2>&1 &
done