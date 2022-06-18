544675c6f971f7399a000e79
  
  
int stringToNumber(String str) => int.parse(str);
_______________________
int stringToNumber(String str) {
  return int.parse(str);
}
_______________________
int stringToNumber(String str) {
  if (str[0] == "-")
    return -(stringToNumber(str.substring(1)));
  if (str.length == 1)
    return (str.codeUnitAt(0) - "0".codeUnitAt(0));
  return (stringToNumber(str.substring(0, str.length - 1)) * 10 + str.codeUnitAt(str.length - 1) - "0".codeUnitAt(0));
}
_______________________
int stringToNumber(String n) => int.parse(n); 
_______________________
int? stringToNumber(String str) => int.tryParse(str);
