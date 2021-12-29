String rnaToDna(String dna) => dna.replaceAll("T", "U");

_____________________________
String rnaToDna(String dna) {
  var rna = dna.replaceAll("T", "U");
  return dna.contains("T") ? rna : dna;
}

_____________________________
String rnaToDna(String dna) {
  String ans = '';
  for (int i = 0; i < dna.length; i++) {
    if (dna[i] == 'T') {
      ans += 'U';
    } else {
      ans += dna[i];
    }
  }
  return ans;
}

_____________________________
String rnaToDna(String dna) {
  var result = dna.replaceAll(RegExp('T'), 'U');
  return result;
}

_____________________________
String rnaToDna(String dna) {
  String rna = "";
  for (int i = 0; i < dna.length; i++) {
    dna[i] == "T"? rna+="U" : rna+=dna[i];
  }
  return rna;
}
