function sortArray(array) {
  const odd = array.filter((x) => x % 2).sort((a,b) => a - b);
  return array.map((x) => x % 2 ? odd.shift() : x);
}
_______________________________________________
function sortArray(array) {
  var odds = [];
  //loop, if it's odd, push to odds array
  for (var i = 0; i < array.length; ++i) {
    if (array[i]%2 !== 0) {
      odds.push(array[i]);
    }
  }
  //sort odds from smallest to largest
  odds.sort(function(a,b){
    return a-b;
  });
  
  //loop through array, replace any odd values with sorted odd values
  for (var j = 0; j < array.length; ++j) {
    if (array[j]%2 !== 0) {
      array[j] = odds.shift();
    }
  }
  
 return array;
}
_______________________________________________
function sortArray(array) {
  var odd = array.filter(elem => elem % 2 !== 0).sort((a, b) => a - b);
  return array.map(elem => elem % 2 === 0 ? elem : odd.shift());
}
_______________________________________________
function sortArray(array) {
  let oddArr = [];
  let evenArr = [];
  let finalArr = [];
  
  for (let i = 0; i < array.length; i++) {
    if (array[i]%2 === 0) {
      evenArr.push(array[i]);
    } else {
      oddArr.push(array[i]);
    }
  }
  oddArr.sort((a, b) => a - b);

  for (let i = 0; i < array.length; i++) {
    if (array[i]%2 === 0) {
      finalArr.push(evenArr.shift());
    } else {
      finalArr.push(oddArr.shift());
    }
  }
  return finalArr;
}
