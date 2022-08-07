59eb1e4a0863c7ff7e000008


O={'&':[0,0,0,1],'|':[0,1,1,1],'^':[0,1,1,0]}
P={'&':([Q,W],[E,R])=>[Q*E,Q*R+W*E+W*R],'|':([Q,W],[E,R])=>[Q*E+Q*R+W*E,W*R],'^':([Q,W],[E,R])=>[Q*R+W*E,Q*E+W*R]}
H=(Q,S,L,M,R,K)=>C[K=1E6*L+1E3*M+R]||(C[K]=P[S[M]](N(Q,S,L,M),N(Q,S,1+M,1+R)))
N=(Q,S,L,R)=>L-R?[...Array(R-L)].reduce(([V,B],_,F)=>(F=H(Q,S,L,L+F,R-1),[V+F[0],B+F[1]]),[0,0]):[Q[L],1^Q[R]]
solve=(Q,S)=>[...S=S.slice(0,Q.length-1)].reduce((D,V,F)=>D+H(Q,S,0,F,S.length-1)[0],0,Q=[...Q].map(V=>'t'==V),C={})
_________________________________________
const c = [1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862, 16796, 58786, 208012, 742900, 2674440, 9694845, 35357670, 129644790, 477638700, 1767263190, 6564120420, 24466267020, 91482563640, 343059613650, 1289904147324, 4861946401452];
const m = [];
function solve(s, ops) {
  if (!m[s]) m[s] = [];
  if (m[s][ops]) return m[s][ops];
  let count = 0;
  for (let i = 0; i < ops.length; i++) {
    const op = ops[i];
    const lS = s.slice(0, i+1);
    const rS = s.slice(i+1);
    const lOps = ops.slice(0, i);
    const rOps = ops.slice(i+1);
    if (op == '&' && (lS == 'f' || rS == 'f'))
      continue;
    else if (op == '|') {
      if (lS == 't') {
        count +=  c[rOps.length];
        continue;
      }
      if (rS == 't') {
        count += c[lOps.length];
        continue;
      }
    }
    const lCount = lOps ? solve(lS, lOps) : +(lS == 't');
    const lTotal = c[lOps.length];
    const rCount = rOps ? solve(rS, rOps) : +(rS == 't');
    const rTotal = c[rOps.length];
    count += op == '&' ? lCount * rCount :
             op == '|' ? lCount * rTotal + rCount * lTotal - lCount * rCount : 
                 /* ^ */ lCount * (rTotal - rCount) + rCount * (lTotal - lCount);
  }
  return m[s][ops] = count;
};
_________________________________________
function solve(s, ops) {
   if (s.length!== ops.length+1) { 
      throw Error;
   }
  let cache  ={t:{t:1,f:0},f:{t:0,f:1}};
  
  
  function calc(str,opers) { 
   if (cache.hasOwnProperty(str+opers))  return cache[str+opers]
    
    let Truths =0;
    let fails = 0;
    
    for (let i= 0;i< opers.length;i++) { 
    let left = calc(str.slice(0,i+1),opers.slice(0,i));
      let right = calc(str.slice(i+1),opers.slice(i+1));
      switch (opers[i]) { 
      case '&': { 
      Truths+=left.t*right.t;
        fails += left.t*right.f + left.f*(right.t+right.f);
        break
      }
      case '|': { 
      Truths +=  left.t * (right.t + right.f) + left.f * right.t;
        fails += left.f*right.f;
        break;
      }
          case '^': { 
          Truths += left.t*right.f+ left.f*right.t;
            fails += left.t * right.t + left.f*right.f;
          
          }
      }
    
    }
   return cache[str+opers] = {t:Truths,f:fails}
  
  }
  return calc(s,ops).t
  
};
