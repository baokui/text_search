mkdir log
date=20200102
time=(00 01 02 03 04 05 06)
for((i=0;i<7;i++))
do
input=VpaOutput_guobk/data_LM/$date/${time[$i]}/*
output=VpaOutput_guobk/data_LM/ngram/$date/${time[$i]}
nohup sh run_join.sh $input $output >> ./log/$date-${time[$i]}.log 2>&1 &
done
