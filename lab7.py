import os
import math
import urllib.request
import matplotlib.pyplot as plt

ACCESSION = 'NC_000913.3'
START, STOP = 1, 10000

enzymes = {
    'EcoRI': ('GAATTC', 1),
    'BamHI': ('GGATCC', 1),
    'HindIII': ('AAGCTT', 1),
    'TaqI': ('TCGA', 1),
    'HaeIII': ('GGCC', 2),
}


def get_sequence():
    if os.path.exists('sequence.fasta'):
        text = open('sequence.fasta').read()
    else:
        url = (f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id={ACCESSION}'
               f'&rettype=fasta&seq_start={START}&seq_stop={STOP}')
        text = urllib.request.urlopen(url).read().decode()
    return ''.join(line.strip() for line in text.splitlines() if not line.startswith('>')).upper()


def digest(seq, site, cut):
    cuts = []
    i = seq.find(site)
    while i != -1:
        cuts.append(i + cut)
        i = seq.find(site, i + 1)
    bounds = [0] + cuts + [len(seq)]
    fragments = [bounds[k + 1] - bounds[k] for k in range(len(bounds) - 1)]
    return cuts, fragments


seq = get_sequence()
print('Sequence length:', len(seq))

results = {}
for name, (site, cut) in enzymes.items():
    cuts, fragments = digest(seq, site, cut)
    results[name] = fragments
    print(f'\n{name}  site {site[:cut]}^{site[cut:]}')
    print('  Number of cleavages:', len(cuts))
    print('  Cleavage positions:', cuts)
    print('  Fragment lengths:', fragments)

ladder = [100, 250, 500, 1000, 1500, 2000, 3000, 5000, 8000, 10000]
lanes = [('Ladder', ladder)] + list(results.items())

lo, hi = math.log(50), math.log(max(len(seq), 10000))
plt.figure(figsize=(9, 7), facecolor='black')
ax = plt.gca()
ax.set_facecolor('black')
for lane, (name, sizes) in enumerate(lanes):
    ax.add_patch(plt.Rectangle((lane + 0.2, 0.97), 0.6, 0.02, color='gray'))
    for size in sizes:
        distance = (hi - math.log(max(size, 50))) / (hi - lo)
        y = 0.95 - 0.9 * distance
        ax.add_patch(plt.Rectangle((lane + 0.2, y), 0.6, 0.006, color='white', alpha=0.8))
        if name == 'Ladder':
            ax.text(lane + 0.1, y, f'{size}', color='white', ha='right', va='center', fontsize=7)
ax.set_xlim(-0.6, len(lanes))
ax.set_ylim(0, 1)
ax.set_xticks([i + 0.5 for i in range(len(lanes))])
ax.set_xticklabels([n for n, _ in lanes], color='white')
ax.set_yticks([])
plt.title('Restriction digest - gel electrophoresis', color='white')
plt.savefig('gel_restriction.png')
plt.show()
