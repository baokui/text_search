userid=$1
input1=$2
input2=$3
input3=$4
input4=$5
Date=$6
hpoutput=VpaOutput_guobk/userhistory_godText/user_join/$Date/user_$userid/
hadoop fs -rmr $hpoutput
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
    -D stream.non.zero.exit.is.failure=false \
    -D mapred.reduce.tasks=5 \
    -D mapred.map.tasks=5 \
    -D mapred.task.timeout=86400000 \
    -D mapreduce.map.memory.mb=2048 \
    -D mapreduce.reduce.memory.mb=4096 \
    -files mapper1.py,reducer1.py \
    -input $input1 \
    -input $input2 \
    -input $input3 \
    -input $input4 \
    -output $hpoutput \
    -mapper "python mapper1.py" \
    -reducer "python reducer1.py"

