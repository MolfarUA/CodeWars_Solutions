52c4dd683bfd3b434c000292


export function isInteresting(n: number, awesomePhrases: number[]): number {
  return checkInteresting(n, awesomePhrases) ? 2 : 
          checkInteresting(n + 1, awesomePhrases) 
          || checkInteresting(n + 2, awesomePhrases) ? 1 : 0;
}

const checkInteresting = (n: number, awesomePhrases: number[]): boolean => {
  const nArr = n.toString().split('').map(Number);
  
  return nArr.length >= 3 && (
      /^\d0+$/.test(n.toString())
      || /^(\d)\1{2,}$/.test(n.toString())
      || awesomePhrases.includes(n)
      || '1234567890'.includes(n.toString())
      || '9876543210'.includes(n.toString())
      || nArr.slice().reverse().every((e, i) => e == nArr[i])
  );
}
_________________________________
export function isInteresting(n: number, awesomePhrases: number[]): number {
  if (checkNumber(n, awesomePhrases)) {
    return 2;
  }
  
  if (checkNumber(n + 1, awesomePhrases) || checkNumber(n + 2, awesomePhrases)) {
    return 1;
  }

  return 0;
}

function checkNumber(n: number, awesomePhrases: number[]): boolean {
  return `${n}`.length > 2 && (
    isNumberFollowedByZeros(n) || 
    areAllDigitEqual(n) || 
    areDigitsSequentialAndIncreamenting(n) || 
    areDigitsSequentialAndDecreamenting(n) || 
    isPalindrome(n) || 
    isAwesomeNumber(n, awesomePhrases)
  );
}

function isNumberFollowedByZeros(n: number): boolean {
  const match = `${n}`.match(/^\d0*$/);
  return match !== null;
}

function areAllDigitEqual(n: number): boolean {
  return new Set([...`${n}`]).size === 1;
}

function areDigitsSequentialAndIncreamenting(n: number): boolean {
  return `01234567890`.includes(`${n}`);
}

function areDigitsSequentialAndDecreamenting(n: number): boolean {
  return `9876543210`.includes(`${n}`);
}

function isPalindrome(n: number): boolean {
  return `${n}` === [...`${n}`].reverse().join("");
}

function isAwesomeNumber(n: number, awesome: number[]): boolean {
  return awesome.includes(n);
}
_________________________________
export function isInteresting(n: number, awesomePhrases: number[]): number {
  const bigNum = /^\d0+$/;
  const sameDig = /^(\d)\1+$/;
  const incSeq = /(^|1)(^|2)(^|3)(^|4|$)(^|5|$)(^|6|$)(^|7|$)(8|$)(9|$)(0|$)/;
  const decSeq = /(^|9)(^|8)(^|7)(^|6|$)(^|5|$)(^|4|$)(^|3|$)(2|$)(1|$)(0|$)/;
  const palindrome = /^(\d)(\d?)(\d?)(\d?)\d?\4\3\2\1$/;
  const res = [bigNum, palindrome, incSeq, decSeq, sameDig];
  if (n >= 100 && res.some(re => re.test(n + '')) || awesomePhrases.some(phrase => n === phrase))
    return 2;
  if (n >= 98 && res.some(re => re.test(n + 2 + '') || re.test(n + 1 + '')) || awesomePhrases.some(phrase => n < phrase && n + 2 >= phrase))
    return 1;
  return 0;
}
