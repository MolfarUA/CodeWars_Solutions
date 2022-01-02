String makeUpperCase(String str) {
  return str.toUpperCase();
}
_____________________________________________
String makeUpperCase(String str) => str!= null && str.isNotEmpty ? str.toUpperCase() : '';
_____________________________________________
String makeUpperCase(String str) {
  int strLength = str.length;
  int strToInt(String s) => s.codeUnits.single;
  List<int> a = [];
  for (int i = 0; i < strLength; i++) {
    if (strToInt(str[i]) >= strToInt('a') &&
        strToInt(str[i]) <= strToInt('z')) {
      a.add(strToInt(str[i]) - 32);
    } else {
      a.add(strToInt(str[i]));
    }
  }
    return String.fromCharCodes([...a]);
}
_____________________________________________
String makeUpperCase(String s) => s.toUpperCase();
