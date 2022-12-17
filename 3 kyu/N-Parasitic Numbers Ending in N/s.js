55df87b23ed27f40b90001e5


const calculateSpecial = (t, i) => {
    let l = 0,
        n = t,
        o = t.toString(i);
    do {
        o = (n = (l = n * t + ~~(l / i)) % i).toString(i) + o
    } while (l != t);
    return o.slice(1)
}
____________________________
const calculateSpecial = (lastDigit, base) => {
  // This assumes lastDigit coming in has form of base 10 regardless...

  // Example calculateSpecial(4,10)
  // We know we multiply this mystery number ending in 4 with 4
  // so ??...?4
  //         x4
  //===========
  //         16
  //        +?0
  //      +???0
  //      .....
  // Since we know the number six will be the only digit in the ones we can deduce
  // 6 is the next digit so:
  // so ??..?64
  //         x4
  //===========
  //         16
  //        240
  // So the next digit is gonna be a 5... and so on until we get to:
  //   ??102564
  //         x4
  //===========
  // From this point, we'll have no carry overs (looking at the 1 btw),
  // and you have to realise, if you were to continue, we'll arrive at
  // another 4... which loops it around and so it suffices to stop here.

  let listOfNumbers = [lastDigit]; // Begin construction of number.
  let carry = 0; // If there is a flow over to the next digit, this will hold it.

  // Loop here until something is done.
  do {
    let product = lastDigit * listOfNumbers[0];
    product += carry; // Add any carry accumulated from the previous calculation.

    let digit = product % base; // This must be the digit in base 10 form of the next digit.
    listOfNumbers.unshift(digit); // Unshift this newly found 'next' (to left) digit number into construct.

    carry = ~~(product / base); // Fancy and more performant way of doing a Math.floor.
  } while (listOfNumbers[0] != 1 || carry != 0);

  // At this point we have an array of numbers in base 10 form.

  const result = listOfNumbers.map(el => el.toString(base)).join('');
  // Mapping each element to the desired base.

  return result;
}
____________________________
// This uses a recursive approach 
// if i = true && d == e and t = 0 then return '' else 
// use our recursive approach.
//  A092697,  A146561, ... (and so on)
// f is used merely for call

// input : trailing digit : d, base : b
// note : not an ideal solution (or even a fast one)
// note : you can use base (b) or just do base 36 as its the highest JS toString supports anyways

// t is reminder, e is where to stop, i is loop. if you change a bit they make tie ;) 

const calculateSpecial = f = (d, b, l = d, t = 0, e = d, i = 0) => 
  i && d == e && !t ? "" : f((d * l + t) % b, b, l, (d * l + t) / b | 0, e, 1) + d.toString(36)
____________________________
function calculateSpecial(digit, base){
  var res = [], n = digit*digit, carry = 0;
  while( n != digit ){
    res.unshift(n%base);
    carry = ~~(n/base);
    n = res[0]*digit + carry
  }
  res.push(digit)
  return res.map( d => d.toString(base) ).join('')

}
