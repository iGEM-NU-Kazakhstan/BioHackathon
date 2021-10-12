import re, random
print("Enter the DNA")
passed = False
while not passed:
    text = input()
    text = text.upper()
    check = set(list(text))
    for i in check:
        if i not in ("A", "T", "C", "G"):
            print("Enter the valid DNA")
            break
        passed = True

restricted_enzs= []
print("How many restriction sites ?")
n = int(input())
while n:
    enz = input().upper()
    for i in enz:
        if i not in ("A", "T", "C", "G") and len(enz) < 3:
            print("PRINT CORRECT RESTRICTION SITES")
            continue
    n -= 1
    restricted_enzs.append(enz)
di = { 
    'TTT': ["TTC"], 
    'TTC': ['TTT'], 
    'TTA': ['TTG'], 
    'TTG': ['TTA'], 
    'TCT': ['TCC', 'TCA', 'TCG'], 
    'TCC': ['TCT', 'TCA', 'TCG'], 
    'TCA': ['TCT', 'TCC', 'TCG'], 
    'TCG': ['TCT', 'TCA', 'TCC'], 
    'TAT': ['TAC'], 
    'TAC': ['TAT'], 
    'TAA': None, 
    'TAG': None, 
    'TGT': ['TGC'], 
    'TGC': ['TGT'], 
    'TGA': None, 
    'TGG': None, 
    'CTT': ['CTC', 'CTA', 'CTG'], 
    'CTC': ['CTT', 'CTA', 'CTG'], 
    'CTA': ['CTC', 'CTT', 'CTG'], 
    'CTG': ['CTC', 'CTA', 'CTT'], 
    'CCT': ['CCC', 'CCA', 'CCG'], 
    'CCC': ['CCT', 'CCA', 'CCG'], 
    'CCA': ['CCC', 'CCT', 'CCG'], 
    'CCG': ['CCC', 'CCA', 'CCT'], 
    'CAT': ['CAC'], 'CAC': ['CAT'], 
    'CAA': ['CAG'], 'CAG': ['CAA'], 
    'CGT': ['CGC', 'CGA', 'CGG'], 
    'CGC': ['CGT', 'CGA', 'CGG'], 
    'CGA': ['CGC', 'CGT', 'CGG'], 
    'CGG': ['CGC', 'CGA', 'CGT'], 
    'ATT': ['ATC', 'ATA'], 
    'ATC': ['ATT', 'ATA'], 
    'ATA': ['ATC', 'ATT'], 
    'ATG': None, 
    'ACT': ['ACC', 'ACA', 'ACG'], 
    'ACC': ['ACT', 'ACA', 'ACG'], 
    'ACA': ['ACC', 'ACT', 'ACG'], 
    'ACG': ['ACC', 'ACA', 'ACT'], 
    'AAT': ['AAC'], 
    'AAC': ['AAT'], 
    'AAA': ['AAG'], 
    'AAG': ['AAA'], 
    'AGT': ['AGC'], 
    'AGC': ['AGT'], 
    'AGA': ['AGG'], 
    'AGG': ['AGA'], 
    'GTT': ['GTC', 'GTA', 'GTG'], 
    'GTC': ['GTT', 'GTA', 'GTG'], 
    'GTA': ['GTC', 'GTT', 'GTG'], 
    'GTG': ['GTC', 'GTA', 'GTT'], 
    'GCT': ['GCC', 'GCA', 'GCG'], 
    'GCC': ['GCT', 'GCA', 'GCG'], 
    'GCA': ['GCC', 'GCT', 'GCG'], 
    'GCG': ['GCC', 'GCA', 'GCT'], 
    'GAT': ['GAC'], 
    'GAC': ['GAT'], 
    'GAA': ['GAG'], 
    'GAG': ['GAA'], 
    'GGT': ['GGC', 'GGA', 'GGG'], 
    'GGC': ['GGT', 'GGA', 'GGG'], 
    'GGA': ['GGC', 'GGT', 'GGG'], 
    'GGG': ['GGC', 'GGA', 'GGT'], 
}
j = 0
while j < len(restricted_enzs):
    enz = restricted_enzs[j]
    le = len(enz)
    inds = [m.start() for m in re.finditer(enz, text)]
    if len(inds) == 0:
        j += 1
    else:
        j = 0
        for ind in inds:
            temp = []
            for i in range(le - 2):
                temp.append(text[ind+i:ind+i+3])
            random_temp = random.randint(0, len(temp)-1)
            k = temp[random_temp]
            while not di[k]:
                random_temp = random.randint(0, len(temp)-1)
                k = temp[random_temp]
            di_arr = di[k]
            random_di = random.randint(0, len(di_arr) - 1)
            swap = di_arr[random_di]
            text = text[:ind + 2 + random_temp] + swap[-1] + text[ind + 3 + random_temp:]
print(f"5' {text} 3'")
compl = {'A':'T','T':'A','C':'G','G':'C'}
def reverser(text):
    x = ''
    for i in text:
        x += compl[i]
    return x
print(f"3' {reverser(text)} 5'")


    