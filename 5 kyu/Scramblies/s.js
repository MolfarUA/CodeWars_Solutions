55c04b4cc56a697bb0000048


function scramble(str1, str2) {
  let occurences = str1.split("").reduce((arr, cur) => { arr[cur] ? arr[cur]++ : arr[cur] = 1; return arr; }, {});
  return str2.split("").every((character) => --occurences[character] >= 0);
}
______________________________
const scramble = (str1, str2) =>
  [...str2].every(val => str2.split(val).length <= str1.split(val).length);
______________________________
function scramble(strToBeChecked, strToCheckFor) {
  let numLetters = {}

  for (const letter of strToCheckFor) {
    if (numLetters[letter]) numLetters[letter]++
    else numLetters[letter] = 1
  }

  for (const letter of strToBeChecked) {
    if (numLetters[letter] && numLetters[letter] !== 0) numLetters[letter]--
  }

  for (const key in numLetters) {
    if (numLetters[key] !== 0) return false
  }

  // Only reaches this far if all good
  return true
}

