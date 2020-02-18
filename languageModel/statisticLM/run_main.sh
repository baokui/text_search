mkdir log
date=20200103
time=(00 01 02 03 04 05 06 07 08 09 10 11)
for((i=0;i<12;i++))
do
input=VpaOutput_guobk/data_LM/$date/${time[$i]}/*
output=VpaOutput_guobk/data_LM/ngram/$date/${time[$i]}
nohup sh run_join.sh $input $output >> ./log/$date-${time[$i]}.log 2>&1 &
done

date=20200102
input=VpaOutput_guobk/data_LM/ngram/$date/*/p*
output=VpaOutput_guobk/data_LM/ngram_day/$date
nohup sh run_join_join.sh $input $output >> ./log/day-$date.log 2>&1 &