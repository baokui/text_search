path_source=zhangfeixue/nlg/userdata/
path_target=VpaOutput_guobk/dabaigou_train_nnlm/
idx=000
input=$path_source/part-00$idx
output=$path_target/00$idx
nohup sh run_join.sh $input $output >> log/00$idx-.log 2>&1 &
'''
mkdir log
Month=202001
for((k=0;k<4;k++))
do
    for((i=0;i<9;i++))
    do
        idx=$k$i
        input=zhangfeixue/shurufa/st_data/$Month/00$idx*
        output=VpaOutput_guobk/dabaigou_train/$Month/00$idx
        nohup sh run_join.sh $input $output >> log/$Month-00$idx-.log 2>&1 &
        echo $input
    done
    i=9
    idx=$k$i
    input=zhangfeixue/shurufa/st_data/$Month/00$idx*
    output=VpaOutput_guobk/dabaigou_train/$Month/00$idx
    nohup sh run_join.sh $input $output >> log/$Month-00$idx-.log 2>&1
    echo $input
done
'''