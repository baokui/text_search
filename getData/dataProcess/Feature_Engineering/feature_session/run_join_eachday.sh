year=$1
month=$2
day=$3
file=$4
input1=VpaOutput_guobk/userhistory_imagemix/user_$file/$year$month/$day/part*
hpoutput=VpaOutput_guobk/userhistory_imagemix/feature/feature_session/$year$month/$day/user_$file/
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
    -files mapper.py,reducer.py,table-trigger.txt,table-search-caption.txt \
    -input $input1 \
    -output $hpoutput \
    -mapper "python mapper.py" \
    -reducer "python reducer.py"