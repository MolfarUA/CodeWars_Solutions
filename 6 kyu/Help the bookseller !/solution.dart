String stockSummary(List<String> lstOfArt, List<String> lstOf1stLetter) {
  if(lstOfArt.length * lstOf1stLetter.length == 0) return '';
  
  final list = lstOf1stLetter.map((letter) {
    final tmpLstOfArt = List.of(lstOfArt);
    tmpLstOfArt.retainWhere((art) => art.startsWith(letter));
    
    if (tmpLstOfArt.isNotEmpty) {
      final sum = tmpLstOfArt
          .map((art) => int.parse(art.replaceAll(RegExp(r'^\w+ '), '')))
          .reduce((v, e) => v + e);     
      return '($letter : $sum)';
    } else {
      return '($letter : 0)';
    }
  });
  return list.join(' - ');
}
________________________________________
String stockSummary(List<String> lstOfArt,List<String> lstOf1stLetter) {
  if (lstOfArt.length == 0 || lstOf1stLetter == 0) return '';
  Map<String, int> categories = Map.fromEntries(lstOf1stLetter.map((key) => MapEntry(key, 0)).toList().cast<MapEntry<String, int>>());
  
  for (var code in lstOfArt) {
    if (categories[code[0]] == null) continue;
    categories[code[0]] += int.tryParse(code.split(' ').last) ?? 0;
  }
  
  return categories.entries.map((e) => ('(${e.key} : ${e.value})')).join(' - ');
}
________________________________________
String stockSummary(List<String> lstOfArt, lstOf1stLetter) {
    if (lstOfArt.length == 0)
        return "";
    String result = "";
    lstOf1stLetter.forEach((String m) {
        int tot = 0;
        lstOfArt.forEach((String l) {
            if (l[0] == m[0]) {
                tot += int.parse(l.split(' ')[1]);
            }
        });
        if (result != "") {
            result += " - ";
        }
        result += "(" + m + " : " + tot.toString() + ")";
    });
    return result;
}
________________________________________
String stockSummary(List<String> lstOfArt, lstOf1stLetter) {
  if (lstOfArt.isEmpty || lstOf1stLetter.isEmpty) {
    return "";
  }
  List<String> result = [];
  for(String letter in lstOf1stLetter) {
    int q = 0;
    lstOfArt.where((x) => x[0] == letter).map((x) => q += int.parse(x.split(' ')[1])).toList();
    result.add('($letter : $q)');
  }
  return result.join(' - ');
}
