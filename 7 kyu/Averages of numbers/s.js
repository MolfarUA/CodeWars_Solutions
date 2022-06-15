function averages(numbers) {
  var final = [];
  if (numbers) {
    for (var i=0; i<numbers.length-1; i++) {
      final.push((numbers[i] + numbers[i+1]) / 2);
    }
  }
  return final;
}
____________________________
function averages(numbers) {
  return numbers ? numbers.map((v, i, a) => (v + a[i + 1]) / 2).slice(0, -1) : [];
}
____________________________
const averages = ($) => $ === null ? [] : $.slice(1).map( (el, i)=> (el + $[i]) / 2 )
____________________________
function averages(numbers) {
  if (!Array.isArray(numbers) || numbers.length < 2) {
    return []
  }
  const result = []
  for (let i = 0; i < numbers.length - 1; i++) {
    result.push((numbers[i] + numbers[i + 1]) / 2)
  }
  return result
}
____________________________
function averages(numbers) {
  let result = [];
  if (!numbers) {
    return result;
  }
  for (let i = 1; i < numbers.length; i += 1) {
    result.push((numbers[i - 1] + numbers[i]) / 2);
  }
  return result;
}
____________________________
const averages = a => validArray(a) ? a.map(avgOfNumbers).slice(0,-1) : []
const validArray = a => a != null && a.length > 1
const avgOfNumbers = (c, i, a) => (c + a[i+1])/2
