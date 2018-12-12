import os, tempfile
from itertools import zip_longest

n = 60000
def grouper(n, iterable, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)

def split():
    with open('data/data.json') as f:
        for i, g in enumerate(grouper(n, f, fillvalue=None)):
            with tempfile.NamedTemporaryFile('w', delete=False) as fout:
                for j, line in enumerate(g, 1): 
                    if line is None:
                        j -= 1 
                        break
                    fout.write(line)
            os.rename(fout.name, 'data/data_{0}.json'.format(i+1)) 

split()

        