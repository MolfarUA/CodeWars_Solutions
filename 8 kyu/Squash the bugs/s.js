56f173a35b91399a05000cb7


function findLongest(str) {
  var spl = str.split(" "),
      longest = 0;
  
  for (var i in spl) {
    if (spl[i].length > longest) {
      longest = spl[i].length;
    }
  }

  return longest;
}
__________________________
const findLongest = s => Math.max(...s.split(" ").map(x => x.length));
__________________________
const findLongest = input => Math.max(...input.split(" ").map(i => i.length));
__________________________
const findLongest = str =>
  Math.max(...str.split(` `).map(val => val.length));
