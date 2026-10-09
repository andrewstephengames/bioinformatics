prot = {
    "UUU": "Phe",
    "UUC": "Phe",
    "UUA": "Leu",
    "UUC": "Leu",
    "UCU": "Ser",
    "UCC": "Ser",
    "UCA": "Ser",
    "UCG": "Ser",
    "UAU": "Tyr",
    "UAC": "Tyr",
    "UAA": "Stop",
    "UAG": "Stop",
    "UGU": "Cys",
    "UGC": "Cys",
    "UGA": "Stop",
    "UGG": "Trp",
    "CUU": "Leu",
    "CUC": "Leu",
    "CUA": "Leu",
    "CUG": "Leu",
    "AUU": "Ile",
    "AUC": "Ile",
    "AUA": "Ile",
    "AUG": "Met",
    "GUU": "Val",
    "GUC": "Val",
    "GUA": "Val",
    "GUG": "Val",
    "CCU": "Pro",
    "CCC": "Pro",
    "CCA": "Pro",
    "CCG": "Pro",
    "ACU": "Thr",
    "ACC": "Thr",
    "ACA": "Thr",
    "ACG": "Thr",
    "GCU": "Ala",
    "GCC": "Ala",
    "GCA": "Ala",
    "GCG": "Ala",
    "CAU": "His",
    "CAC": "His",
    "CAA": "Gln",
    "CAG": "Gln",
    "AAU": "Asn",
    "AAC": "Asn",
    "AAA": "Lys",
    "AAG": "Lys",
    "GAU": "Asp",
    "GAC": "Asp",
    "GAA": "Glu",
    "GAG": "Glu",
    "CGU": "Arg",
    "CGC": "Arg",
    "CGA": "Arg",
    "CGG": "Arg",
    "AGU": "Ser",
    "AGC": "Ser",
    "AGA": "Arg",
    "AGG": "Arg",
    "GGU": "Gly",
    "GGC": "Gly",
    "GGA": "Gly",
    "GGG": "Gly",
}

s = "AUGGGUCGACUGCAA"
t = ""

i=0
ok=0
step = 1
while (i< len(s)):
    pr = s[i:i+3]
    if pr in prot:
        value = prot[pr]
        if pr == "AUG":
            ok = 1
            step = 3
        if value == "Stop":
            break
        if ok == 1:
            t += f"{value}, "

    i+=step

print(t)
