let dna_to_rna = String.map (function 'T' -> 'U' | c -> c)

_____________________________
let dna_to_rna str =
  Str.global_replace (Str.regexp "[T]") "U" str;;
  
_____________________________
let dna_to_rna dna = String.map (fun c -> if c = 'T' then 'U' else c) dna

_____________________________
let dna_to_rna = Str.global_replace (Str.regexp "T") "U"

_____________________________
let dna_to_rna = String.map (fun x -> if x = 'T' then 'U' else x)
