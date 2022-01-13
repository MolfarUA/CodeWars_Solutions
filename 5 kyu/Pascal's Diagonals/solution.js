function generateDiagonal(n, l){
  if (l === 0){
    return [];
  }
  const firstDiag = new Array(l);
  firstDiag.fill(1)
  const allDiags = [];
  allDiags.push(firstDiag);
  for (let i = 1; i <= n; i ++){
    allDiags.push([1]);
    for (let j = 1; j < l; j ++){
      allDiags[i][j] = allDiags[i][j-1] + allDiags[i-1][j];
    }
  }
  
  return (allDiags[n])
}

generateDiagonal(3, 7)
_______________________________
function generateDiagonal(n, l){
  let matrix = [];
  let len = n+l;
  
  
  for(let i=0;i<len;i++){
    matrix[i] = [];
    for(let j = 0; j<len;j++){
      if(i>=j){
        matrix[i][j] = 1;
      }else{
        matrix[i][j] = 0;
      }
    }
  }
  
  for(let i=0; i<len-1;i++){
    for(let j=0;j<len-1;j++){
      matrix[i+1][j+1] = matrix[i][j]+matrix[i][j+1];
    }
  }
  
  let arr = [];
  for(let i=n; i<len;i++){
    arr.push(matrix[i][n]);
  }
  return arr;
}
_______________________________
function generateDiagonal(n, l){
  let res = new Array(l).fill(1)
  while(n>0){
    n--
    let c = 0
    res = res.map(v => {
      c += v
      return c
    })
  }
  return res
}
_______________________________
function generateDiagonal(n, l){
  let arr = [1];
  for (let i = 1; i < l; i++) {
    arr.push(arr[arr.length - 1] * (n + i) / i);
  }
  return l ? arr : [];
}
_______________________________
function generateDiagonal(n, k) {
  const res = [];
  
  for (let i = 0; i < k; ++i) {
    if (!i) res.push(1);
    else res.push(res[i-1] * ++n / i);
  }
  
  return res;
}
_______________________________
function fact(n){
  let res = 1n;
  for(let i=2n ; i<=n ; i++){
    res *= i;
  }
  return res;
}

function rising_fact(n, d){
  let res = 1n;
  for(let i=n ; i<n+d ; i++){
    res *= i;
  }
  return res;
}

function generateDiagonal(n, l){
  let res=[];
  n = BigInt(n);
  l = BigInt(l);
  for(let i=1n ; i<=l ; i++){
    res.push(Number(rising_fact(i, n) / fact(n)));
  }
  return res;
}
