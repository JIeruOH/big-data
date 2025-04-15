from cassandra.cluster import Cluster
import sys

cluster = Cluster(['cassandra-server'])
session = cluster.connect()

session.execute("""
    CREATE KEYSPACE IF NOT EXISTS bigdata 
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
""")
session.set_keyspace('bigdata')

session.execute("""
    DROP TABLE IF EXISTS terms;
""")
session.execute("""
    DROP TABLE IF EXISTS docs;
""")
session.execute("""
    DROP TABLE IF EXISTS constants;
""")

session.execute("""
    CREATE TABLE terms (
        term TEXT,
        doc_id TEXT,
        freq INT,
        PRIMARY KEY (term, doc_id)
    )
""")
session.execute("""
    CREATE TABLE docs (
        doc_id TEXT PRIMARY KEY,
        title TEXT,
        len INT,
    )
""")
session.execute("""
    CREATE TABLE constants (
        var TEXT PRIMARY KEY,
        value INT,
    )
""")

for line in sys.stdin:
    line = line.strip()
    line = line.split('\t')
    if line[0] == 'const':
        var, value = line[1:]
        session.execute(
            "INSERT INTO constants (var, value) VALUES (%s, %s)", (var, int(value))
        )
    elif line[0] == 'docs':
        doc_id, title, ln = line[1:]
        session.execute(
            "INSERT INTO docs (doc_id, title, len) VALUES (%s, %s, %s)", (doc_id, title, int(ln))
        )

    else:
        term, doc_id, freq = line[1:]
        session.execute(
            "INSERT INTO terms (term, doc_id, freq) VALUES (%s, %s, %s)", (term, doc_id, int(freq))
        )
