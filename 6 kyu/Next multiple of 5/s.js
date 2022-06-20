604f8591bf2f020007e5d23d


const nextMultipleOfFive = n => {
  switch (n % 5) {
      case 0: return 2 * n || 5;
      case 1: return 4 * n + 1;
      case 2: return 2 * n + 1;
      case 3: return 4 * n + 3;
      case 4: return 8 * n + 3;
  }
}
_______________________________
const nextMultipleOfFive = n => {
  let check = a => parseInt(a, 2) % 5 == 0 && a != 0;
  let arr = [];
  
  function generateBin(n){
  var arr = [];
  var k = parseInt("1".repeat(n),2);
  for(var i = 0; i <= k; i++){
    arr.push(i.toString(2).padStart(n,'0'));
  }
  return arr;
};
  
  for (let i = 1; i < 4; i++){
    arr = arr.concat(generateBin(i));
  };
  
  let i = 0;
  while(!check(n.toString(2) + arr[i])){
    i++;
  };
  
  return parseInt(n.toString(2) + arr[i], 2);
}
_______________________________
const nextMultipleOfFive = n => {
  
  if (n===0) {
    return 5
  }
  
    let binaryN = n.toString(2); //Input as binary
  
    let binaryN1 = binaryN + 1; // Input binary + 1
    let binaryN0 = binaryN + 0; // Input binary + 0
  
    let binaryN10 = binaryN1 + 0; // Input binary + 10
    let binaryN00 = binaryN0 + 0; // Input binary + 00
    let binaryN11 = binaryN1 + 1; // Input binary + 11
    let binaryN01 = binaryN0 + 1; // Input binary + 01
  
    let binaryN101 = binaryN10 + 1; // Input binary + 101
    let binaryN100 = binaryN10 + 0; // Input binary + 100
    let binaryN001 = binaryN00 + 1; // Input binary + 001
    let binaryN000 = binaryN00 + 0; // Input binary + 000
    let binaryN111 = binaryN11 + 1; // Input binary + 111
    let binaryN110 = binaryN11 + 0; // Input binary + 110
    let binaryN010 = binaryN01 + 1; // Input binary + 010
    let binaryN011 = binaryN01 + 0; // Input binary + 011
  
    let godNumbers = /[50]$/ //regex to check last digit
    
    let checkerN1  = parseInt(binaryN1,2);
    let checkerN0  = parseInt(binaryN0,2);
  
    let checkerN10  = parseInt(binaryN10,2);
    let checkerN00  = parseInt(binaryN00,2);
    let checkerN11  = parseInt(binaryN11,2);
    let checkerN01  = parseInt(binaryN01,2);
  
    let checkerN101  = parseInt(binaryN101,2);
    let checkerN100  = parseInt(binaryN100,2);
    let checkerN001  = parseInt(binaryN001,2);
    let checkerN000  = parseInt(binaryN000,2);
    let checkerN111  = parseInt(binaryN111,2);
    let checkerN110  = parseInt(binaryN110,2);
    let checkerN010 = parseInt(binaryN010,2)
    let checkerN011 = parseInt(binaryN011,2)
   
  if (checkerN1.toString().match(godNumbers)) {
         return checkerN1
     } else if (checkerN0.toString().match(godNumbers)) {
       return checkerN0
     } else if (checkerN01.toString().match(godNumbers)) {
       return checkerN01 } 
        else if (checkerN00.toString().match(godNumbers)) {
       return checkerN00 
     } else if (checkerN11.toString().match(godNumbers)) {
        return checkerN11 
      } else if (checkerN10.toString().match(godNumbers)) {
       return checkerN10    
    }   else if (checkerN101.toString().match(godNumbers)) {
       return checkerN101   
    } else if (checkerN100.toString().match(godNumbers)) {
       return checkerN100   
    } else if (checkerN001.toString().match(godNumbers)) {
       return checkerN001   
    } else if (checkerN000.toString().match(godNumbers)) {
       return checkerN000    
    } else if (checkerN111.toString().match(godNumbers)) {
       return checkerN111    
    } else if (checkerN110.toString().match(godNumbers)) {
       return checkerN110  
    } else if (checkerN010.toString().match(godNumbers)) {
       return checkerN010    
    } else if (checkerN011.toString().match(godNumbers)) {
       return checkerN011    
    } else {
      return 'failure'
    }
};

console.log(nextMultipleOfFive(0))
