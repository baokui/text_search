userid=$1
Month=$2
Day=$3
input1=VpaOutput_guobk/session_join_android_godText/$Month/$Day/*/part*
hpoutput=VpaOutput_guobk/userhistory_godText/user_$userid/$Month/$Day/
hadoop fs -rmr $hpoutput
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
    -D stream.non.zero.exit.is.failure=false \
    -D mapred.reduce.tasks=5 \
    -D mapred.map.tasks=5 \
    -D mapred.task.timeout=86400000 \
    -D mapreduce.map.memory.mb=2048 \
    -D mapreduce.reduce.memory.mb=4096 \
    -files mapper_user$userid.py,reducer.py \
    -input $input1 \
    -output $hpoutput \
    -mapper "python mapper_user$userid.py" \
    -reducer "python reducer.py"

