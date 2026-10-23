import random

s = ""
f = open("sequence.fasta")
for line in f:
    if not line.startswith(">"):
        s += line.strip().upper()
f.close()

reads = []
for i in range(20000):
    n = random.randint(100, 150)
    p = random.randint(0, len(s) - n)
    reads.append(s[p:p+n])

mn = 10
pre = {}
suf = {}
for r in reads:
    a = r[:mn]
    b = r[-mn:]
    if a in pre:
        pre[a].append(r)
    else:
        pre[a] = [r]
    if b in suf:
        suf[b].append(r)
    else:
        suf[b] = [r]

unused = set(reads)
contigs = []

while len(unused) > 0:
    c = unused.pop()
    inc = set()
    inc.add(c)

    go = 1
    while go == 1:
        go = 0
        i = max(0, len(c) - 150)
        while i <= len(c) - mn and go == 0:
            k = c[i:i+mn]
            if k in pre:
                L = len(c) - i
                ext = ""
                best = ""
                for r in pre[k]:
                    if r not in inc and len(r) > L and r[:L] == c[i:] and len(r) - L > len(ext):
                        ext = r[L:]
                        best = r
                if ext != "":
                    c = c + ext
                    inc.add(best)
                    go = 1
            i += 1

    go = 1
    while go == 1:
        go = 0
        e = min(len(c), 150)
        while e >= mn and go == 0:
            k = c[e-mn:e]
            if k in suf:
                ext = ""
                best = ""
                for r in suf[k]:
                    if r not in inc and len(r) > e and r[-e:] == c[:e] and len(r) - e > len(ext):
                        ext = r[:len(r)-e]
                        best = r
                if ext != "":
                    c = ext + c
                    inc.add(best)
                    go = 1
            e -= 1

    for r in list(unused):
        if r in c:
            unused.remove(r)
    contigs.append(c)

contigs.sort(key=len, reverse=True)

print("Genome length:", len(s))
print("Reads taken:", len(reads))
print (reads[0])
print (reads[1])
print("Contigs built:", len(contigs))
print("Longest contig:", len(contigs[0]))
print("Longest contig found inside original:", contigs[0] in s)
print("Missing nucleotides:", len(s) - len(contigs[0]))
print("Identical to original:", contigs[0] == s)

f = open("assembled.fasta", "w")
f.write(">assembled\n")
f.write(contigs[0] + "\n")
f.close()
