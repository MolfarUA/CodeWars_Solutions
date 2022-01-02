String smash(words) => words.join(' ');

_____________________________________
String smash(words) {
  return words.join(' ');
}

_____________________________________
String smash(words) {
  String phrase = '';
  words.forEach((w) => phrase += '${w} ');
  return phrase.trim();
}
