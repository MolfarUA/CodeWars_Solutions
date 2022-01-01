export function order(words:String):String{
  return words.split(' ')
              .sort((a,b)=> +a.match(/\d/)-+b.match(/\d/))
              .join(' ')
}

_____________________________________________
export function order(words:String):String{
  const wordsArray = words.split(' ');
  const wordsSorted = wordsArray.sort((a,b) => _calculatePosition(a)-_calculatePosition(b) );
  
  return wordsSorted.join(' ');
}

function _calculatePosition(word: string): number {
  const numberString = /[0-9]{1}/.exec(word)[0];
  return parseInt(numberString, 10);
}

_____________________________________________
export function order(words:String):String{  
  return words.split(' ')
    .sort((l, r) =>  +/\d/.exec(l)[0] -  +/\d/.exec(r)[0])
    .join(' ');
}

_____________________________________________
export function order(words:String):String{
  const isANum = (letter:String) => !isNaN(Number(letter));
  return words.split(" ").sort((a:String, b:String) => Number(a.split("").find(isANum)) - Number(b.split("").find(isANum))).join(" ")
}

_____________________________________________
export function order(words:String):String{
  let wordArray: string[] = words.split(' ');
  let resultArray: string[] = [];
  for(let i=1; i<=words.length; i++) {
    wordArray.forEach((word) => {
      if (word.indexOf(i.toString()) >= 0) {
        resultArray.push(word);
      }
    });
  };
  return resultArray.join(' ');
}
