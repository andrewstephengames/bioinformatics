import random

random.seed(7)


def rnd(n):
    return ''.join(random.choice('ACGT') for _ in range(n))


tes = {'TE1': rnd(40), 'TE2': rnd(35), 'TE3': rnd(45), 'TE4': rnd(30)}

dna = ''
truth = []


def add(x):
    global dna
    p = len(dna)
    dna += x
    return p


add(rnd(30))
s1 = add(tes['TE1'][:20])
s2 = add(tes['TE2'])
add(tes['TE1'][20:])
truth.append(('TE2', s2, s2 + len(tes['TE2']) - 1, 'nested inside TE1'))
truth.append(('TE1', s1, len(dna) - 1, 'split by TE2'))

add(rnd(50))
s3 = add(tes['TE3'][:35])
s4 = add(tes['TE4'])
truth.append(('TE3', s3, s3 + 34, 'last 10 bases overwritten by TE4'))
truth.append(('TE4', s4, s4 + len(tes['TE4']) - 1, 'overlaps TE3'))

add(rnd(60))
s1b = add(tes['TE1'])
truth.append(('TE1', s1b, s1b + len(tes['TE1']) - 1, 'intact'))
add(rnd(40))


def detect(dna, tes, k=8):
    found = []
    for name, te in tes.items():
        heads = [i for i in range(len(dna)) if dna.startswith(te[:k], i)]
        tails = [i + k - 1 for i in range(len(dna)) if dna.startswith(te[-k:], i)]
        for h in heads:
            after = [t for t in tails if t > h and t - h < 3 * len(te)]
            if after:
                e = after[0]
                kind = 'complete' if e - h + 1 == len(te) else 'interrupted (something inserted)'
                found.append((name, h, e, kind))
                tails.remove(e)
            else:
                m = 0
                while h + m < len(dna) and m < len(te) and dna[h + m] == te[m]:
                    m += 1
                found.append((name, h, h + m - 1, 'truncated (end missing)'))
        for t in tails:
            found.append((name, None, t, 'truncated (start missing)'))
    return sorted(found, key=lambda x: x[1] if x[1] is not None else x[2])


print('DNA length:', len(dna))
print(dna)
print('\nInserted:')
for n, s, e, note in sorted(truth, key=lambda x: x[1]):
    print(f'{n}: {s}-{e}  {note}')
print('\nDetected:')
for n, s, e, kind in detect(dna, tes):
    print(f'{n}: {s}-{e}  {kind}')
