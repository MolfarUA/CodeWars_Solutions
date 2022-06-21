5263c6999e0f40dee200059d


function getPINs(observed) {
  return observed.split('')
  .map( t => ({
    '0': [ '0', '8' ],
    '1': [ '1', '2', '4' ],
    '2': [ '1', '2', '3', '5' ],
    '3': [ '2', '3', '6' ],
    '4': [ '1', '4', '5', '7' ],
    '5': [ '2', '4', '5', '6', '8' ],
    '6': [ '3', '5', '6', '9' ],
    '7': [ '4', '7', '8' ],
    '8': [ '5', '7', '8', '9', '0' ],
    '9': [ '6', '8', '9' ]
  }[t]))
  .reduce((pre, cur)=> [].concat.apply([], pre.map(t => cur.map(g => t + g))));
}
______________________________
"use strict"

function getPINs(observed) {
  const adjacent = {
    1: ["1", "2", "4"], 2: ["2", "1", "5", "3"], 3: ["3", "2", "6"], 4: ["4", "1", "5", "7"],
    5: ["5", "2", "4", "6", "8"], 6: ["6","3", "5", "9"], 7: ["7", "4", "8"],
    8: ["8", "5", "7", "9", "0"], 9: ["9", "6", "8"], 0: ["0", "8"]
  };

  let possibleDigits = observed.split("").map(pin => adjacent[pin]);
  
  
  if (possibleDigits.length < 2) {
    return possibleDigits[0];
  }
  
  function arraysCombination (arr1, arr2) {
    const result = [];
    
    for (let i in arr1) {
      for (let j in arr2) {
        result.push(arr1[i] + arr2[j])
      }
    }
    
    return result;
  }
  
  function findPins (array) {
    
    if (array.length < 3) {
        return arraysCombination(array[0], array[1]);
    } else {
      let previousDigit = array[0];
      let remainingDigits = array.slice(1)
      return arraysCombination(previousDigit, findPins(remainingDigits))
    }
  }
  
  return findPins(possibleDigits);
}
______________________________
function getPINs(obs) {
  const combinations = {
    0: ["0", "8"],
    1: ["1", "2", "4"],
    2: ["1", "2", "3", "5"],
    3: ["2", "3", "6"],
    4: ["4", "7", "5", "1"],
    5: ["5", "2", "4", "6", "8"],
    6: ["6", "5", "3", "9"],
    7: ["7", "4", "8"],
    8: ["7", "8", "9", "5", "0"],
    9: ["9", "8", "6"],
  };
  let result = combinations[obs[0]];

  obs
    .slice(1)
    .split("")
    .forEach((num) => {
      const newResult = [];
      combinations[num].forEach((av) => {
        result.forEach((currentValue) => {
          newResult.push(`${currentValue}${av}`);
        });
      });

      result = newResult;
    });

  return result;
}
