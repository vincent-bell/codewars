def find_it(seq):
    freq = {}
    for n in seq: freq[n] = 1 if n not in freq else freq[n] + 1
    for k in freq:
        if freq[k] % 2 != 0: return k
