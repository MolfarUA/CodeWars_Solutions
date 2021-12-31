function hamming (n) {
  var seq = [1];
  var i2 = 0, i3 = 0, i5 = 0;
  for (var i = 1; i < n; i++) {
    var x = Math.min(2 * seq[i2], 3 * seq[i3], 5 * seq[i5]);
    seq.push(x);
    if (2 * seq[i2] <= x) i2++;
    if (3 * seq[i3] <= x) i3++;
    if (5 * seq[i5] <= x) i5++;
  }
  return seq[n-1];
}

___________________________________________________
function hamming (n) {
  let seq = [1];
  let i2 = 0, i3 = 0, i5 = 0;
  for (let i = 1; i < n; i++) {
    let x = Math.min(2 * seq[i2], 3 * seq[i3], 5 * seq[i5]);
    seq.push(x);
    if (2 * seq[i2] <= x) i2++;  //<= can be replaced by ==
    if (3 * seq[i3] <= x) i3++;
    if (5 * seq[i5] <= x) i5++;
  }
  return seq.pop()}

___________________________________________________
function hamming(number) {
    let args = [], i, j, k;
    args[0] = 1, i = j = k = 0;

    for (let itterator = 1; itterator < number; itterator++) {
        args[itterator] = Math.min(args[i] * 2, args[j] * 3, args[k] * 5);
        if (args[itterator] === args[i] * 2)  i++;
        if (args[itterator] === args[j] * 3)  j++;
        if (args[itterator] === args[k] * 5)  k++;
    }
    return args[number - 1];
}

___________________________________________________
// function hamming (n) {
//   let arr =[]
  
//     let i=1
//   while(arr.length !== n){
 
//     let num = i
    
//       while(num%2 === 0 && num !== 0 ){
//       num = num/ 2
//     }

//       while(num %3 ===0 && num !== 0 ){
//         num = num /3
//       }
//       while(num % 5 === 0 && num !== 0 ){
//         num= num /5
//       }
//         if(num=== 1) arr.push(i)
//     i++
//   }
   
//   return arr[arr.length-1]
    
  
// }


function hamming (n) {
  let arr =[1];
  let idx2 =0;
  let idx3=0;
  let idx5 =0;
  
  for(let i =1; i < n;i++){
    let ele = Math.min(2*arr[idx2], 3*arr[idx3], 5*arr[idx5])
    arr.push(ele)
    if(ele >= 2*arr[idx2]) idx2++
    if(ele >= 3*arr[idx3]) idx3++
    if(ele >= 5*arr[idx5]) idx5++
  }
return arr[n -1]
}


___________________________________________________
let hamsSorted = []

function buildHamsSorted() {
    let hams = []
    for (i=0;i<36;i++) {
        for (j=0;j<36;j++) {
            for (k=0;k<36;k++) {
                hams.push(Number(Math.pow(2,i)*Math.pow(3,j)*Math.pow(5,k)))
            }
        }
    }
    hamsSorted = hams.sort(function(a, b){return a-b})
}

function hamming (n) {
    if (hamsSorted.length === 0) { buildHamsSorted() }
    return hamsSorted[n-1]
}

___________________________________________________
function hamming(n) {
  let secuence = [1],
      i2 = 0,
      i3 = 0,
      i5 = 0
  
  for(let i = 1; i < n; i++) {
    let x = Math.min(2 * secuence[i2], 3 * secuence[i3], 5 * secuence[i5])
    
    secuence.push(x)
    
    if(2 * secuence[i2] <= x) i2++
    if(3 * secuence[i3] <= x) i3++
    if(5 * secuence[i5] <= x) i5++
  }
  
  return secuence[n - 1]
}
