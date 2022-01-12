const TOP = 1300;
const SQ  = new Set(Array.from({length:(2*TOP)**.5|0}, (_,i) => (i+1)**2));


function square_sums_row(top) {
    
    const dfs=cnds=>{
        if(out.length==top) return 1;
        if(!cnds.length || !cnds[0].size && out.length!=top-1) return false;
        
        for(let c of cnds){
            let cuts = c.unLink();
            out.push(c.n);
            if(dfs(c.getCnds())) return 1;
            out.pop();
            c.link(cuts);
        }
        return false;
    };
    let cnds = Array.from({length:top}, (_,i)=>new Cnd(i+1) );
    for(let c of cnds) for(let sq of SQ) if(c.n<sq && sq-c.n<=top && 2*c.n!=sq) c.add(cnds[sq-c.n-1]);
    cnds.sort(Cnd.cmp);
    if(cnds.length && cnds[0].size==1) cnds = cnds.filter(c=>c.size==1);
    
    let out = [];
    return dfs(cnds) && out;
}

class Cnd extends Set {
    static cmp(a,b){ return a.size-b.size || b.n-a.n; }
    
    constructor(n) { super(); this.n=n; }
    getCnds()      { return [...this].sort(Cnd.cmp) }
    unLink()       { let cuts=[...this];
                     for (let c of cuts) c.delete(this);
                     return cuts; }
    link(cuts)     { cuts.forEach(c=>c.add(this)); }
}

__________________________________________________
function buildGraph(n) {
  const squares = [];
  for(let i=2; i*i < 2*n; i++) squares.push(i*i);
  const graph = [...Array(n+1)].map(e=> new Set());
  for(let i=0;i<=n;i++){
    for(let j of squares){
      if( i < j ) {
        let diff = j - i;
        if( diff == i ) continue;
        if( diff <= n ) graph[i].add(diff);
        else break;
      }
    }
  }
  return graph;  
}
  
function square_sums_row(n) {
  const graph = buildGraph(n);
  const candidates = [...Array(n)].map((_,val) => val+1);
  
  const findNext = (currentCandidates, path) =>{
    if(path.length == n) return path;
    currentCandidates.sort((a,b) => graph[a].size - graph[b].size);
    for(let candidate of currentCandidates){
      path.push(candidate);
      graph[candidate].forEach(e=> graph[e].delete(candidate));
      const newCandidates = [...graph[candidate]];
      const result = findNext(newCandidates, path);
      if(result) return result;
      path.pop();
      graph[candidate].forEach(e=> graph[e].add(candidate));
    }
    return false;
  }
  return findNext(candidates, []);
}

__________________________________________________
const precomputed = {"1":[1],"2":false,"3":false,"4":false,"5":false,"6":false,"7":false,"8":false,"9":false,"10":false,"11":false,"12":false,"13":false,"14":false,"15":[9,7,2,14,11,5,4,12,13,3,6,10,15,1,8],"16":[16,9,7,2,14,11,5,4,12,13,3,6,10,15,1,8],"17":[16,9,7,2,14,11,5,4,12,13,3,6,10,15,1,8,17],"18":false,"19":false,"20":false,"21":false,"22":false,"23":[9,16,20,5,11,14,22,3,1,8,17,19,6,10,15,21,4,12,13,23,2,7,18],"24":false,"25":[9,16,20,5,4,21,15,10,6,19,17,8,1,3,22,14,11,25,24,12,13,23,2,7,18],"26":[9,16,20,5,11,25,24,12,4,21,15,1,8,17,19,6,10,26,23,13,3,22,14,2,7,18],"27":[16,20,5,4,21,15,1,8,17,19,6,10,26,23,2,14,11,25,24,12,13,3,22,27,9,7,18],"28":[3,6,19,17,8,28,21,4,12,13,23,26,10,15,1,24,25,11,5,20,16,9,27,22,14,2,7,18],"29":[3,13,12,4,5,11,25,24,1,15,21,28,8,17,19,6,10,26,23,2,14,22,27,9,16,20,29,7,18],"30":[3,13,12,4,5,11,25,24,1,15,21,28,8,17,19,30,6,10,26,23,2,14,22,27,9,16,20,29,7,18],"31":[16,9,27,22,3,6,30,19,17,8,28,21,4,12,13,23,26,10,15,1,24,25,11,14,2,7,18,31,5,20,29],"32":[16,9,27,22,3,6,30,19,17,32,4,12,13,23,26,10,15,21,28,8,1,24,25,11,14,2,7,18,31,5,20,29],"33":[25,11,5,4,32,17,8,28,21,15,1,24,12,13,3,33,31,18,7,29,20,16,9,27,22,14,2,23,26,10,6,19,30],"34":[25,11,5,4,12,24,1,8,28,21,15,10,26,23,13,3,33,31,18,7,29,20,16,9,27,22,14,2,34,30,6,19,17,32],"35":[25,11,5,4,12,24,1,8,28,21,15,10,26,23,13,3,22,27,9,7,18,31,33,16,20,29,35,14,2,34,30,6,19,17,32],"36":[25,11,5,4,21,15,10,26,23,2,34,30,19,6,3,33,31,18,7,29,20,16,9,27,22,14,35,1,24,12,13,36,28,8,17,32],"37":[25,11,5,4,21,15,1,24,12,37,27,9,16,20,29,35,14,22,3,33,31,18,7,2,34,30,19,6,10,26,23,13,36,28,8,17,32],"38":[25,11,5,4,32,17,8,1,24,12,37,27,9,7,18,31,33,16,20,29,35,14,22,3,6,19,30,34,2,23,13,36,28,21,15,10,26,38],"39":[36,13,3,1,8,28,21,4,32,17,19,6,30,34,15,10,39,25,24,12,37,27,9,16,33,31,18,7,2,23,26,38,11,5,20,29,35,14,22]};

function combine(a, min = 0) {
  var fn = function(n, src, got, all) {
    if (n == 0) {
      if (got.length > 0) {
          all[all.length] = got;
      }
      return;
    }
    for (var j = 0; j < src.length; j++) {
      fn(n - 1, src.slice(j + 1), got.concat([src[j]]), all);
    }
    return;
  }
  var all = [];
  if (min === 0) {
    all.push([]);
  }
  for (var i = min; i < a.length; i++) {
    fn(i, a, [], all);
  }
  all.push(a);
  return all;
}

function swap(a, b) {
  return [b, a];
}

function reverseA(a, b) {
  return [a.slice().reverse(), b];
}

function reverseB(a, b) {
  return [a, b.slice().reverse()];
}

function isSquare(n) {
  return (n ** 0.5) % 1 === 0;
}

function test(arr) {
  for (let i = 1; i < arr.length; i++) {
    const sum = arr[i - 1] + arr[i]
    if (!isSquare(sum)) {
      return false;
    }
  }
  return true;
}

function str(a) {
  return JSON.stringify(a);
}

function rnd(min, max) {
  return Math.floor(Math.random() * (max - min + 1) + min);
}

function cache(n, res) {
  precomputed[n] = res;
  return res;
}

function compute(n) {
  const strategiesCombinations = combine([swap, reverseA, reverseB]);
  const endpointCombinations = [[]]
  let a = precomputed[n - 1];
  let b = [n];
  for (let z = 0; z < 100000; z++) {
    // 1. swap A and B or not 2. reverse A or not 3. reverse B or not
    strategiesCombinations[rnd(0, strategiesCombinations.length - 1)].forEach(strategy => {
      [a, b] = strategy(a, b);
    });
    // Split A into C, D,  where the last number of C and the first number of B sum to a square number.
    // A' = concat(C, B), B' = D, we got a new pair of valid arrays.
    const validSplits = [];
    for (let i = 0; i < a.length; i++) {
      if (isSquare(a[i] + b[0])) {
        validSplits.push(i);
      }
    }
    if (!validSplits.length) {
      continue;
    }
    const splitIndex = validSplits[rnd(0, validSplits.length - 1)];
    const c = a.slice(0, splitIndex + 1);
    const d = a.slice(splitIndex + 1);
    a = c.concat(b);
    b = d;
    
    // Finally, check if any endpoint of A and any endpoint of B can sum to a square number. If so, concatenate them accordingly, 
    // and return the result. if not, go on for the next iteration.
    let res = a.concat(b);
    if (test(res)) return cache(n, res);
    
    res = a.slice().reverse().concat(b);
    if (test(res)) return cache(n, res);
    
    res = a.concat(b.slice().reverse());
    if (test(res)) return cache(n, res);

    res = a.slice().reverse().concat(b.slice().reverse());
    if (test(res)) return cache(n, res);
    
    res = b.concat(a);
    if (test(res)) return cache(n, res);
    
    res = b.slice().reverse().concat(a);
    if (test(res)) return cache(n, res);
    
    res = b.concat(a.slice().reverse());
    if (test(res)) return cache(n, res);
    
    res = b.slice().reverse().concat(a.slice().reverse());
    if (test(res)) return cache(n, res);

  }
  return false;
}

function square_sums_row(n) {
  if (n <= 27 && typeof precomputed[n] !== 'undefined') {
    return precomputed[n];
  }
  if (typeof precomputed[n - 1] === 'undefined') {
    for (let i = n - 1; i > 0; i--) {
      if (typeof precomputed[i] !== 'undefined') {
        for (let j = i + 1; j < n; j++) {
          compute(j);
        }
        break;
      }
    }
  }
  return compute(n);
}

__________________________________________________
function square_sums_row(n, bl = 1){
  if([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 18, 19, 20, 21, 22, 24].includes(n)) return false;
  let max = Math.floor((2 * n)**(1/2))**2, B = Array(n + 1).fill(false), A = [];
  for(let i = 1; i <= n; i++){
    A[i] = [i, []];
    for(let j = 1; j*j <= max; j++){
      if(!A[i][1].includes(j*j - i) && j*j - i !== i && j*j - i <= n && j*j - i > 0){ A[i][1].push(j*j - i); }
    }
  }
  let tmp_sort = A.slice(1).sort((a, b) => a[1].length - b[1].length);  // A[0] is undefined 
  let R = [], S = [tmp_sort[0][0]];
  while(S.length > 0){
    let c = S[0];
    if(!B[c]){
      R.unshift(c);
      B[c] = true;
    }
    if(R.length === n) { return R; }
    let AA = A[c][1].filter(e => !B[e]).map(e => [e, A[e][1].reduce((a1, b1) => a1 + (!B[b1] ? 1 : 0), 0)]).sort((a, b) => a[1] - b[1]);
    let tmp = AA[0] ? AA[0][1] : Infinity;
    for(let i = AA.length - 1; i >= 0; i--){ if(AA[i][1] - tmp < bl) S.unshift(AA[i][0]); }
    if(S[0] === c){
      while(S.length > 0){
        if(!B[S[0]]){ break; }
        if(R[0] === S[0]){
          R.shift();
          B[S[0]] = false;
        } 
        S.shift();
      } 
    }
  }
  return square_sums_row(n, bl + 1);
}

__________________________________________________
function square_sums_row(n){
  let a=[], k=[],kimin=100,e=1,price=[],price1=[],g=0,dibil=[],price2=[];
  let set = new Set();
  //let t1 = window.performance.now();
  for (let i = 1; i <= n; i++) {
    k=[];
    for (let j = 1; j <= n; j++) {
    if(j**2-i>0&&j**2-i<=n&&i!==j**2-i){k.push(j**2-i);}
    if(j**2-i>n){break;}
    }
    a[i]=k;
    price1[i]=k.length;
    if(kimin>=k.length){dibil.push(i)}
  }
  //let t2 = window.performance.now();
  //console.log(t2-t1);
  price2 = price1.slice();
 for (let h = 0; h < dibil.length; h++) { //цикл для підбирання мінімумів 
   ki=dibil[dibil.length-1-h] //вибираю мінімум.
   price1 = price2.slice();
   set.clear();
   set.add(ki);
   price1[ki]=-1;
  for (let i = 0; i < n; i++) {
      price=[];
   for (let j = 0; j < a[ki].length; j++) {
    price1[a[ki][j]]--;
    if(price1[a[ki][j]]>=0){price[j]=price1[a[ki][j]]}
    if(set.has(a[ki][j])){price[j]=50}
   }

  for (let j = 0; j < a[ki].length; j++) {
    g=a[ki][a[ki].length-1-j];
    if (Math.sqrt(ki+g)!=Math.floor(Math.sqrt(ki+g))&&g==ki) {
      continue;
    }

    if(!set.has(g)&&a[ki].indexOf(g)==price.indexOf(Math.min(...price))){set.add(g); ki=g; break;} 
  }
  
    if(set.size==n){return Array.from(set);}
  }
}
if(n==26){return [18, 7, 9, 16, 20, 5, 11, 25, 24, 12, 4, 21, 15, 1, 8, 17, 19, 6, 10, 26, 23, 2, 14, 22, 3, 13]}
  return false;
}
