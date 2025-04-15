import sys

terms = {}

for line in sys.stdin:
    line = line.strip()
    line = line.split('\t')
    if line[0] == 'const':
        avg = line[1]
        print(f'const\tavg\t{avg}')
    elif line[0] == 'docs':
        doc_id, title, ln = line[1:]
        print(f'docs\t{doc_id}\t{title}\t{ln}')
    else:
        term, doc_id = line[1:]
        if (term, doc_id) not in terms:
            terms[(term, doc_id)] = 0
        terms[(term, doc_id)] += 1

for (term, doc_id), freq in terms.items():
    print(f"terms\t{term}\t{doc_id}\t{freq}")
