int duplicateCount(String text){
  text = text.toLowerCase();
  Map<String, int> letterMap = {};
  text.split("").forEach((letter){
    if(letterMap[letter] == null)
       letterMap[letter] = 1;
    else
       letterMap[letter]+=1;
  });
  return letterMap.values.where((value)=>value>1).length;
}
_________________________
int duplicateCount(String text){
    // print(text.toUpperCase().runes.toList()..sort());
  final data = {};

  for(final c in text.toUpperCase().runes) {
    if(data[c] == null) {
      data[c] = 1;
    }else{
      data[c]++;
    }
  }

  return data.values.fold(0,(acc, v) =>  v > 1 ? ++acc : acc);

}
________________________________
int duplicateCount(String text){
  final countMap = <String,int>{};
  for(final char in text.split('')){
    countMap[char.toLowerCase()] ??= 0;
    countMap[char.toLowerCase()] += 1;
  }
  return countMap.values.where((e)=>e>1).length;
}
___________________
int duplicateCount(String text){
  int counter = 0;
  String lowerText = text.toLowerCase();
  while (lowerText.length > 0) {
    if (lowerText[0].allMatches(lowerText).length > 1) {
      counter ++;
    }
    lowerText = lowerText.replaceAll(lowerText[0], '');
  }
  return counter;
}
____________________
int duplicateCount(String text){
    int count = 0;
    int points = 0;
    text = text.toLowerCase();
    List<String> result = text.split('');

    for (int i = 0; i < text.length; i++) {
      for (int k = 0; k < result.length; k++) {
        if ((result[k] == text[i])) points++;
      }
      if (points > 1) count++;
      points = 0;
      result.removeWhere((val) => val == text[i]);
    }

    return count;
}
