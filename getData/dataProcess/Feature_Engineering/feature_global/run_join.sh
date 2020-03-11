idx=$1
Date=$2
input1=VpaOutput_guobk/userhistory_imagemix/user_join/$Date/user_$idx/part*
hpoutput=VpaOutput_guobk/userhistory_imagemix/feature/feature_global/$Date/user_$idx
hadoop fs -rmr $hpoutput
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
    -D stream.non.zero.exit.is.failure=false \
    -D mapred.reduce.tasks=5 \
    -D mapred.map.tasks=5 \
    -D mapred.task.timeout=86400000 \
    -D mapreduce.map.memory.mb=2048 \
    -D mapreduce.reduce.memory.mb=2048 \
    -files mapper.py,reducer.py,keywords.txt \
    -input $input1 \
    -output $hpoutput \
    -mapper "python mapper.py" \
    -reducer "python reducer.py"

