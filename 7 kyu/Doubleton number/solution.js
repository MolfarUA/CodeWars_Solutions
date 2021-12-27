const isDoubleton = n => new Set(String(n)).size === 2 ;
const doubleton = n => isDoubleton(n+1) ? n+1 : doubleton(n+1) ;

#############
const doubleton = (num) => new Set(String(++num).split("")).size === 2 ? num : doubleton(num)

############
function doubleton(num) {
  while (true) {
    num++;
    if (new Set(String(num)).size === 2) {
      return num;
    }
  }
}  

###############
const doubleton = num =>
  new Set([...`${++num}`]).size === 2 ? num : doubleton(num);

################
with(require('ramda'))
  var isDN = pipe(String, uniq, length, equals(2))
  const doubleton =f= n => isDN(++n) ? n : f(n)
  
#############
function doubleton(num){
  let myNum = num + 1;
  while (true){
    let myNum2 = myNum.toString().split('')
    let tem = new Set(myNum2)
    if(Array.from(tem).length === 2){
      return myNum;
    }
    myNum ++;
  }
}  
