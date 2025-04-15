#!/bin/bash

INPUT_PATH=/index/data
TMP_PATH=/tmp/index/output1
MAPPER=/app/mapreduce/mapper1.py
REDUCER=/app/mapreduce/reducer1.py

source .venv/bin/activate
hdfs dfs -rm -r $TMP_PATH
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming*.jar \
    -files $MAPPER,$REDUCER \
    -input $INPUT_PATH \
    -output $TMP_PATH \
    -mapper "python3 mapper1.py" \
    -reducer "python3 reducer1.py"

hdfs dfs -cat $TMP_PATH/part-* | python3 /app/app.py
