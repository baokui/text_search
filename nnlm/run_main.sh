path_source=zhangfeixue/nlg/userdata/
path_target=VpaOutput_guobk/dabaigou_train_nnlm
input=$path_source/part-00*
output=$path_target/00$idx
nohup sh run_join.sh $input $output >> log/00$idx.log 2>&1 &
