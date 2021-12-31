function listPosition(word) {
    let res = 0;

    for (let i = 0; i < word.length; i++) {
        res += positionFirstLetter(word.slice(i));
    }

    return res + 1;
}

function positionFirstLetter(word) {
    let res = 0;
    let earlierLetters = [];

    for (let i = 1; i < word.length; i++) {
        if (word.charCodeAt(i) < word.charCodeAt(0) && !earlierLetters.includes(word[i])) {
            earlierLetters.push(word[i]);
        }
    }

    earlierLetters.forEach((e) => {
        res += numOfPerms(word.replace(e, ""));
    });

    return res;
}

function numOfPerms(word) {
    let denominator = 1;

    const letterCounts = [...word].reduce((a, e) => {
        a[e] = a[e] ? a[e] + 1 : 1;
        return a;
    }, {});

    for (const key in letterCounts) {
        denominator *= factorial(letterCounts[key]);             // accounting for repeating letters
    }

    return factorial(word.length) / denominator;
}

function factorial(n) {
    if (n === 1) {
        return 1;
    }

    return n * factorial(n - 1);
}

___________________________________________________
const factorialCache = [1, 1];
const factorial = (n) => {
  if (!factorialCache[n]) {
    factorialCache[n] = n * factorial(n - 1);
  }
  return factorialCache[n];
}

const getCharacterFrequencyLookup = (chars) => {
  const result = {}
  
  for (const char of chars) {
    result[char] = result[char] ? result[char] + 1 : 1;
  }
  
  return result;
}

const getUniquePermutationCount = (chars, charFrequencyLookup) => {
  const numerator = factorial(chars.length - 1);
  const denominator = Object.values(charFrequencyLookup).reduce(
    (acc, freq) => factorial(freq) * acc, 
    1
  ) 
  return numerator / denominator;
}

const listPosition = (word) => {
  if (word.length === 1) return 1;
  
  const unsortedChars = word.split('');
  const characterFrequencyLookup = getCharacterFrequencyLookup(unsortedChars);
  let sortedChars = word.split('').sort();
  let currentUnsortedCharIndex = 0;
  
  if (sortedChars.join('') === word) return 1;
  
  let result = 1;
  
  while (currentUnsortedCharIndex < word.length) {
    for (let i = 0; i < sortedChars.length; i++) {
      const currentUnsortedChar = unsortedChars[currentUnsortedCharIndex];
      const currentSortedChar = sortedChars[i];
      
      if (currentUnsortedChar === currentSortedChar) {
        sortedChars = [...sortedChars.slice(0, i), ...sortedChars.slice(i + 1)];
        characterFrequencyLookup[currentSortedChar]--;
        currentUnsortedCharIndex++;
        break;
      } else {
        const permutationCount = getUniquePermutationCount(sortedChars, characterFrequencyLookup);
        result += permutationCount;
      }
    }
  }
  
  return result
}

___________________________________________________
const factorial = (n) => n < 2 ? 1 : n * factorial(n - 1);

const getCharacterFrequencyLookup = (chars) => {
  const result = {}
  
  for (const char of chars) {
    result[char] = result[char] ? result[char] + 1 : 1;
  }
  
  return result;
}

const getUniquePermutationCount = (chars, charFrequencyLookup) => {
  const numerator = factorial(chars.length - 1);
  const denominator = Object.values(charFrequencyLookup).reduce(
    (acc, freq) => factorial(freq) * acc, 
    1
  ) 
  return numerator / denominator;
}

const listPosition = (word) => {
  if (word.length === 1) return 1;
  
  const unsortedChars = word.split('');
  const characterFrequencyLookup = getCharacterFrequencyLookup(unsortedChars);
  let sortedChars = word.split('').sort();
  let currentUnsortedCharIndex = 0;
  
  if (sortedChars.join('') === word) return 1;
  
  let result = 1;
  
  while (currentUnsortedCharIndex < word.length) {
    for (let i = 0; i < sortedChars.length; i++) {
      const currentUnsortedChar = unsortedChars[currentUnsortedCharIndex];
      const currentSortedChar = sortedChars[i];
      
      if (currentUnsortedChar === currentSortedChar) {
        sortedChars = [...sortedChars.slice(0, i), ...sortedChars.slice(i + 1)];
        characterFrequencyLookup[currentSortedChar]--;
        currentUnsortedCharIndex++;
        break;
      } else {
        const permutationCount = getUniquePermutationCount(sortedChars, characterFrequencyLookup);
        result += permutationCount;
      }
    }
  }
  
  return result
}

___________________________________________________
function factorialize(n) {
  let tot = n;
  let i = n;
  while (i > 1) {
    tot*=--i
  }
  return tot
}

function getPermutationsNumber(chars) {
  const p = factorialize(chars.length);
  const dupes = chars.reduce((acc, curr) => {
    acc[curr] = (acc[curr] || 0) + 1;
    return acc;
  }, {})
  const factorializedDupes = Object.values(dupes).map(factorialize).reduce((acc, curr) => acc * curr);
  return p/factorializedDupes
}

function listPosition(word) {
  const arr = word.split('');

  const res = arr.reduce((position, char, i) => {
    const wordSoFar = arr.slice(i)
    const restOfWord = wordSoFar.slice(1);
    const lowerRankingLetters = [...new Set(restOfWord.filter(x => x < char))];

    lowerRankingLetters.forEach(letter => {
      const index = wordSoFar.findIndex((x) => x === letter);
      const wordWithoutLetter = [...wordSoFar]; wordWithoutLetter.splice(index, 1);
      if (wordWithoutLetter.length) {
        const permutations = getPermutationsNumber(wordWithoutLetter);
        position += permutations
      }
    });
    return position;
  },0)
  return res + 1
}

___________________________________________________
let factorial = num =>( num < 0 ? -1 : (num == 0 ? 1 : num * factorial(num - 1)))
let smallerThan = str => str.split('').reduce((total, curr,i) => total += curr.charCodeAt(0) < str.charCodeAt(0) ? 1 : 0, 0)

let occurence = str =>{
  return str.split('').reduce((counts, curr) => {
    counts[curr] ? counts[curr]++ :  counts[curr] = 1
    return counts
  }, {})
}


function listPosition(word) {
  //Return the anagram list position of the word

  let index = 1
  for(let i=0, slicedWord=''; i<word.length; i++){
    slicedWord = word.slice(i, word.length)
//     console.log(slicedWord)
//     console.log(smallerThan(slicedWord))
//       console.log(factorial(slicedWord.length-1)) 
//   console.log(Object.values(occurence(slicedWord)).reduce((total,curr) =>  total* factorial(curr), 1)  )
    index += smallerThan(slicedWord) 
            * factorial(slicedWord.length-1)
            / Object.values(occurence(slicedWord)).reduce((total,curr) =>  total* factorial(curr), 1)
  }

  return index;
  

}
