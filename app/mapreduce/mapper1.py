import sys
import re


def tokenize(text):
    return re.findall(r'\w+', text.lower())


avg = []
for line in sys.stdin:
    line = line.strip()
    try:
        doc_id, title, text = line.split('\t', 2)
        terms = tokenize(text)
        print(f'docs\t{doc_id}\t{title}\t{len(terms)}')
        for term in terms:
            print(f"terms\t{term}\t{doc_id}")
        avg.append(len(terms))
    except:
        pass
print(f'const\t{sum(avg) // len(avg)}')
