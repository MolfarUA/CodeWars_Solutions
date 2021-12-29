def dna_to_rna(dna)
  dna.gsub('T','U')
end

_____________________________
def dna_to_rna(dna)
  dna.tr("T","U")
end

_____________________________
def dna_to_rna(dna)
 chars = dna.chars
 rna = ""
 chars.each do |c|
   c == "T" && c = "U"
   rna << c
 end
  rna
end

_____________________________
def dna_to_rna(dna)
  dna.gsub(/T/, 'U')
end

_____________________________
def dna_to_rna(dna)
  dna.chars.map { |char| char == "T" ?  char = "U"  : char}.join
end
