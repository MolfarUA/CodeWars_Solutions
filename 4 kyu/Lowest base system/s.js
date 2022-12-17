58bc16e271b1e4c5d3000151


function getMinBase(n) {
  for(let i=Math.ceil(Math.log2(n)); i>1; i--) {
    let root=Math.round(findRoot(n,i));
    if([...'1'.repeat(i)].reduce((s,_)=>s*root+1,0)===n) return root;
  }
}

function findRoot(n,i) {
  var l=1, r=Number.MAX_SAFE_INTEGER;
  while((r-l)/l>1e-12) {
    let m=(r+l)/2, g=(Math.pow(m,i)-1)/(m-1);
    g<n?l=m:r=m;
  }
  return (r+l)/2;
}
______________________________________
function getMinBase (n) {
  const root = Math.round(Math.sqrt(n))
  for (let i = 2; i <= root;i++) {
    if (changeBase(n, i)) return i
  }
  return n -1
}

function changeBase (n, base) {
  if (n % base !== 1) return false
  return (n > base) ? changeBase(Math.floor(n / base), base) : n === base || n === 1
}
______________________________________
function getMinBase (n) {
    let ans = n-1;
    let limit = Math.floor(n**0.5);
    for (let i=2; i<=limit; i++){
        let b = Math.floor(n**(1/i));
        if (b<=1) break;
        let a1 = 1-b**(i+1);
        let a2 = n*(1-b);
        if (String(a1).length>=10){
            a1 = Math.round((1-b**(i+1))/1000)*1000;
            a2 = Math.round(n*(1-b)/1000)*1000;
        }
        if (a1==a2){
            ans = b;
        }
    }
    return ans;
}
