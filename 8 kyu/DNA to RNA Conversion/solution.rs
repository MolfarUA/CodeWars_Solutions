fn dna_to_rna(dna: &str) -> String {
 dna.replace("T", "U")
}

_____________________________
fn dna_to_rna(dna: &str) -> String {
    dna.chars().map(char_conversion).collect()
}

fn char_conversion(c: char) -> char {
    if c == 'T' {
        return 'U';
    }
    
    c
}

_____________________________
fn new_char(c: char) -> char {
    return if c == 'T' { 'U' } else { c };
} 

fn dna_to_rna(dna: &str) -> String {
    let vec: Vec<char> = dna.chars().map(new_char).collect();
    let resultStr: String = vec.into_iter().collect();
    
    return resultStr;
}
      
_____________________________
fn dna_to_rna(dna: &str) -> String {
    let mut rna = String::new();
    dna.chars().for_each(|c| rna.push(if c == 'T' { 'U' } else { c }));
    rna
}
