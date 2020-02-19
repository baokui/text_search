input0=$1
hpoutput=$2
hadoop fs -rmr $hpoutput
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
    -D stream.non.zero.exit.is.failure=false \
    -D mapred.reduce.tasks=1 \
    -D mapred.map.tasks=5 \
    -D mapred.task.timeout=86400000 \
    -D mapreduce.map.memory.mb=2048 \
    -D mapreduce.reduce.memory.mb=4096 \
    -files mapper1.py,mapper_join.py \
    -input $input0 \
    -output $hpoutput \
    -mapper "python mapper1.py" \
    -reducer "python mapper_join.py"

