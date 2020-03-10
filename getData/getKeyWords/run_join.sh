input1=VpaOutput_guobk/session_join_android_godText/*/*/*/part*
hpoutput=VpaOutput_guobk/godText/keywords
mars="hdfs://MarsNameNode2"
hadoop fs -rmr $hpoutput
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
    -D stream.non.zero.exit.is.failure=false \
    -D mapred.reduce.tasks=5 \
    -D mapred.map.tasks=5 \
    -D mapred.task.timeout=86400000 \
    -D mapreduce.map.memory.mb=4096 \
    -D mapreduce.reduce.memory.mb=2048 \
    -D yarn.nodemanager.vmem-check-enabled=false \
    -D yarn.nodemanager.vmem-pmem-ratio=5 \
    -archives "$mars/user/ml_research/zuolin/tools2/jieba.tar.gz#jieba" \
    -files mapper.py,reducer.py \
    -input $input1 \
    -output $hpoutput \
    -mapper "python mapper.py" \
    -reducer "python reducer.py"