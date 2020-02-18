mkdir log
date=20200104
time=(12 13 14 15 16 17 18 19 20 21 22 23)
for((i=0;i<12;i++))
do
input=VpaOutput_guobk/data_LM/$date/${time[$i]}/*
output=VpaOutput_guobk/data_LM/ngram/$date/${time[$i]}
nohup sh run_join.sh $input $output >> ./log/$date-${time[$i]}.log 2>&1 &
done

date=20200104
input=VpaOutput_guobk/data_LM/ngram/$date/*/p*
output=VpaOutput_guobk/data_LM/ngram_day/$date
nohup sh run_join_join.sh $input $output >> ./log/day-$date.log 2>&1 &

input=VpaOutput_guobk/data_LM/ngram_day/*/p*
output=VpaOutput_guobk/data_LM/ngram_all
nohup sh run_join_join.sh $input $output >> ./log/day-$date.log 2>&1 &

input=VpaOutput_guobk/data_LM/ngram_all1/p*
output=VpaOutput_guobk/data_LM/ngram_all2
nohup sh run_filter.sh $input $output >> ./log/day-all1.log 2>&1 &