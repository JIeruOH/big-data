from pyspark.sql import SparkSession
import sys
import math

k1 = 1.0
b = 0.75


def bm25(N, df, k1, b, tf, dl, dl_avg):
    return math.log((N + 0.5) / (df + 0.5)) * ((k1 + 1) * tf) / (k1 * ((1 - b) + b * dl / dl_avg) + tf)


query = sys.argv[1].split()

spark = SparkSession.builder \
    .master("local") \
    .getOrCreate()

const = spark.read \
    .format("org.apache.spark.sql.cassandra") \
    .options(table="constants", keyspace="bigdata") \
    .load()

terms = spark.read \
    .format("org.apache.spark.sql.cassandra") \
    .options(table="terms", keyspace="bigdata") \
    .load()

documents = spark.read \
    .format("org.apache.spark.sql.cassandra") \
    .options(table="docs", keyspace="bigdata") \
    .load()

avg = const.filter("var = 'avg'").collect()[0]['value']
N = documents.count()
documents = documents.rdd.map(lambda row: (row['doc_id'], (row['len'], row['title']))).collectAsMap()

docs = {}
for term in set(query):
    term = term.lower()
    found = terms.filter(f"term='{term}'")
    df = found.count()
    for i in found.collect():
        doc = i['doc_id']
        if doc not in docs:
            docs[doc] = 0
        ln = documents[doc][0]
        docs[doc] += bm25(N, df, k1, b, i['freq'], ln, avg)
docs = sorted(((score, doc) for doc, score in docs.items()), reverse=True)

for i, (_, doc) in enumerate(docs[:10]):
    title = documents[doc][1]
    print(f'{i + 1}) {doc} {title}')
