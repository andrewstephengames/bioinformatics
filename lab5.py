import os
import random
import math
import urllib.request
import matplotlib.pyplot as plt

ACCESSION = 'NM_002046'


def get_sequence():
    if os.path.exists('sequence.fasta'):
        text = open('sequence.fasta').read()
    else:
        url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id={ACCESSION}&rettype=fasta'
        text = urllib.request.urlopen(url).read().decode()
    return ''.join(line.strip() for line in text.splitlines() if not line.startswith('>'))[:3000]


def exercise1(seq):
    samples = []
    for _ in range(10):
        size = random.randint(100, min(3000, len(seq)))
        start = random.randint(0, len(seq) - size)
        samples.append(seq[start:start + size])

    sizes = [len(s) for s in samples]
    print('Sample sizes:', sizes)

    lo, hi = math.log(100), math.log(3000)
    plt.figure(figsize=(8, 6), facecolor='black')
    ax = plt.gca()
    ax.set_facecolor('black')
    for lane, size in enumerate(sizes):
        distance = (hi - math.log(size)) / (hi - lo)
        y = 0.95 - 0.85 * distance
        ax.add_patch(plt.Rectangle((lane + 0.2, 0.97), 0.6, 0.02, color='gray'))
        ax.add_patch(plt.Rectangle((lane + 0.2, y), 0.6, 0.012, color='white'))
        ax.text(lane + 0.5, y - 0.03, f'{size} bp', color='white', ha='center', fontsize=8)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 1)
    ax.set_xticks([i + 0.5 for i in range(10)])
    ax.set_xticklabels([f'S{i + 1}' for i in range(10)], color='white')
    ax.set_yticks([])
    plt.title('Gel electrophoresis simulation', color='white')
    plt.savefig('gel.png')
    plt.show()


def find_repeats(seq):
    found = []
    for u in range(3, 6):
        i = 0
        while i + 2 * u <= len(seq):
            unit = seq[i:i + u]
            n = 1
            while seq[i + n * u:i + (n + 1) * u] == unit:
                n += 1
            if n >= 2:
                if 6 <= n * u <= 10:
                    found.append((i, i + n * u - 1, unit, n))
                i += n * u
            else:
                i += 1
    return sorted(found)


def exercise2(seq):
    repeats = find_repeats(seq)
    for start, end, unit, n in repeats:
        print(f'{start}-{end}  {unit} x {n}  {seq[start:end + 1]}')
    print('Total repeats found:', len(repeats))


seq = get_sequence()
print('Sequence length:', len(seq))
print('\nExercise 1')
exercise1(seq)
print('\nExercise 2')
exercise2(seq)
