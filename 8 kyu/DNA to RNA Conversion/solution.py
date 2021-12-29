def dna_to_rna(dna):
    return dna.replace('T', 'U')
  
___________________________
DNAtoRNA = lambda d: d.replace("T", "U")

___________________________
def DNAtoRNA(dna):
    return "".join(["U" if c=="T" else c for c in dna])
  
___________________________
def DNAtoRNA(dna):
    RNA= ""
    i = 0
    for i in dna:
        if i == "T":
            RNA = RNA + "U"
        else:
            RNA = RNA + i
    return RNA
        
___________________________
dna_dict = {
    'T': 'U',
    'A': 'A',
    'C': 'C',
    'G': 'G'
}

def DNAtoRNA(dna):
    rna = []
    for letter in dna:
        rna.append(dna_dict[letter])
    return "".join(rna)
  
___________________________
def dna_to_rna(dna):
    tns = dna.maketrans('T', 'U')
    return dna.translate(tns)
  
___________________________
def dna_to_rna(dna):
    broken = list(dna)
    broken = ["U" if x == "T" else x for x in broken]
    return ''.join(broken)
  
___________________________
def dna_to_rna(dna):
    string = ""
    if len(dna) == 0 :
        return ""
    else:
        for i in dna:
            if i == "T" or i == "t":
                string +="U"
            else:
                string += i
        return string
