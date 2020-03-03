input0=$1
input1=$2
input2=$3
input3=$4
Year=$5
Month=$6
Day=$7
Hour=$8
hpoutput="VpaOutput_guobk/session_join_android/"$Year$Month"/"$Day"/"$Hour
#input1="/storage/sogou/desktop/imeservice/vpare/"$Year$Month"/"$Year$Month$Day"/*"$Month"-"$Day"_"$Hour"*.lzo"
#input2="/cloud/dt/pingback/ping/djt-pb-log/vpapb_android_shouji/"$Year$Month"/"$Year$Month$Day"/*"$Year$Month$Day$Hour"*.lzo"
input4=/storage/sogou/desktop/imeservice/vpa.venus.odin.sogou/$Year$Month/$Year$Month$Day/*$Year-$Month-${Day}_$Hour*.lzo
hadoop fs -rmr $hpoutput
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
    -D stream.non.zero.exit.is.failure=false \
    -D mapred.reduce.tasks=50 \
    -D mapred.map.tasks=5 \
    -D mapred.task.timeout=86400000 \
    -D mapreduce.map.memory.mb=2048 \
    -D mapreduce.reduce.memory.mb=4096 \
    -files mapper_join.py,reducer_join.py \
    -input $input0 \
    -input $input1 \
    -input $input2 \
    -input $input3 \
    -input $input4 \
    -output $hpoutput \
    -mapper "python mapper_join.py" \
    -reducer "python reducer_join.py"

