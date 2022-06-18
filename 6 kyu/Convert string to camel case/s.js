function toCamelCase(str){
  return str.replace(/[-_](.)/g, (_, c) => c.toUpperCase());
}
________________________
function toCamelCase(str){
  return str.split(/-|_/g).map((w, i) => (i > 0 ? w.charAt(0).toUpperCase() : w.charAt(0)) + w.slice(1)).join('');
}
________________________
function toCamelCase(str){
 let arr = [];
  if (str.includes('-')) {
    arr = str.split('-');
  } else arr = str.split('_');

  arr.forEach((word, index) => {
    if (index > 0) arr[index] = word[0].toUpperCase() + word.slice(1);
  });

  return arr.join('');
}
________________________
function toCamelCase(str){
  const wordParts =  str.includes("_")
    ? str.split("_")
    : str.split("-");
  
  const mapCasingTransform = (word, wordIndex) => {
    if (wordIndex === 0) {
      return word;
    }
    
    const wordLetters = word.split("");
    
    wordLetters[0] = wordLetters[0].toUpperCase();
    
    return wordLetters.join("");
  }
  
  return wordParts
    .map(mapCasingTransform)
    .join("");''
}
