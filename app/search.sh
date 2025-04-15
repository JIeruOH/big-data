#!/bin/bash

echo "This script will include commands to search for documents given the query using Spark RDD"

source .venv/bin/activate

export PYSPARK_PYTHON=/usr/bin/python3
export PYSPARK_DRIVER_PYTHON=/usr/bin/python3

spark-submit \
    --master yarn \
    --deploy-mode client \
    --archives /app/.venv.tar.gz#.venv \
    --conf spark.sql.extensions=com.datastax.spark.connector.CassandraSparkExtensions \
    --packages com.datastax.spark:spark-cassandra-connector_2.12:3.5.1 \
    --conf spark.cassandra.connection.host=cassandra-server \
    query.py "$1"