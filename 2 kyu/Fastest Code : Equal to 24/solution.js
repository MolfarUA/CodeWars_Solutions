function equalTo24(...numbers) {
  const exp = numbers.slice()

  function is24(n){
    if (n==1) return +numbers[0].toFixed(4) === 24

    for (let i=0; i<n; i++){
      for (let j=i+1; j<n; j++){
        let a, b, expa, expb // temp storage
        a = numbers[i]
        b = numbers[j]
        numbers[j] = numbers[n-1]
        expa = exp[i]
        expb = exp[j]
        exp[j] = exp[n-1]
        
        exp[i] = "(" + expa + "+" + expb + ")"
        numbers[i] = a + b
        if (is24(n - 1)) return true
        
        exp[i] = "(" + expa + "-" + expb + ")"
        numbers[i] = a - b
        if (is24(n - 1)) return true
        
        exp[i] = "(" + expb + "-" + expa + ")"
        numbers[i] = b - a
        if (is24(n - 1)) return true
        
        exp[i] = "(" + expa + "*" + expb + ")"
        numbers[i] = a * b
        if (is24(n - 1)) return true
        
        if (b!==0) {
          exp[i] = "(" + expa + "/" + expb + ")"
          numbers[i] = a / b
          if (is24(n - 1)) return true
        }
        
        if (a!==0) {
          exp[i] = "(" + expb + "/" + expa + ")"
          numbers[i] = b / a
          if (is24(n - 1)) return true
        }
        
        numbers[i] = a
        numbers[j] = b
        exp[i] = expa
        exp[j] = expb
      }
    }
    return false
  }
  
  let result = is24(4)
  
  return result ? exp[0] : "It's not possible!"
}
_____________________________________________
const OPS = {
  '+': (a, b) => a + b,
  '-': (a, b) => a - b,
  '*': (a, b) => a * b,
  '/': (a, b) => a / b
}
const SYMS = Object.keys(OPS);
const EPSILON = 1e-9;

function equalTo24(a,b,c,d){
  return equals([a,b,c,d], [a,b,c,d].map(String), 24) || "It's not possible!";

  function equals(nums, exprs, target){
    if(nums.length === 1) return Math.abs(nums[0] - target) < EPSILON ? exprs[0] : null;
    let a, b, aExpr, bExpr;
    for(let i = 0; i < nums.length; ++i){
      [a] = nums.splice(i, 1);
      [aExpr] = exprs.splice(i, 1);
      for(let j = 0; j < nums.length; ++j){
        [b] = nums.splice(j, 1);
        [bExpr] = exprs.splice(j, 1);
        for(let op of SYMS){
          nums.push(OPS[op](a, b));
          exprs.push(`(${aExpr}${op}${bExpr})`);
          let result = equals(nums, exprs, target);
          if(result) return result;
          else{
            nums.pop();
            exprs.pop();
          }
        }
        nums.splice(j, 0, b);
        exprs.splice(j, 0, bExpr);
      }
      nums.splice(i, 0, a);
      exprs.splice(i, 0, aExpr);
    }
  }
}
_____________________________________________
function equalTo24(...aceg){
  const ops = {
    '+': (a,b) => a + b,
    '-': (a,b) => a - b,
    '*': (a,b) => a * b,
    '/': (a,b) => a / b,
  }
  
  for (const b in ops)
    for (const d in ops)
      for (const f in ops) 
        for (const [a,c,e,g] of permutations(aceg)) {
          const [B,D,F] = [ops[b],ops[d],ops[f]]
          let result
          makeExp(a,B,c,D,e,F,g).forEach((elem,i) => {
            if (elem === 24) {
              result = makeString(a,b,c,d,e,f,g)[i]
              return
            }
          })
          if (result) return result
        }
          
  return "It's not possible!"
}
function makeExp(a,b,c,d,e,f,g) {
  return [ 
  f(d(b(a,c),e),g),
  d(b(a,c),f(e,g)),
  b(a,d(c,f(e,g))),
  b(a,f(d(c,e),g)),
  f(b(a,d(c,e)),g)]
}
function makeString(a,b,c,d,e,f,g) {
  return [
  `((${a}${b}${c})${d}${e})${f}${g}`,
  `(${a}${b}${c})${d}(${e}${f}${g})`,
  `${a}${b}(${c}${d}(${e}${f}${g}))`,
  `${a}${b}((${c}${d}${e})${f}${g})`,
  `(${a}${b}(${c}${d}${e}))${f}${g}`]
}

function permutations (arr, perms = []) {
  if (arr.length === 1) return [arr]
  for (let i = 0; i < arr.length; i++)
    arr.indexOf(arr[i]) === i && (perms = perms.concat(
      permutations(arr.slice(0, i).concat(arr.slice(i + 1)))
        .map(x => [arr[i]].concat(x))
    ))
  return perms
}
_____________________________________________
let orderMix = (x,o1,y,o2,z,o3,w) => ({
    '((x1y)2z)3w': ()=> o3(o2(o1(x,y),z),w),
    '(x1y)2(z3w)': ()=> o2(o1(x,y),o3(z,w)),
    '(x1(y2z))3w': ()=> o3(o1(x,o2(y,z)),w),
    'x1(y2(z3w))': ()=> o1(x,o2(y,o3(z,w))),
    'x1((y2z)3w)': ()=> o1(x,o3(o2(y,z),w))
  }),
  op = {
    '+': (a,b)=>a+b,
    '-': (a,b)=>a-b,
    '*': (a,b)=>a*b,
    '/': (a,b)=>a/b
  }
function equalTo24(a,b,c,d){
  for (let [x,y,z,w] of [
    [a,b,c,d],[a,b,d,c],[a,c,b,d],[a,c,d,b],[a,d,b,c],[a,d,c,b],
    [b,a,c,d],[b,a,d,c],[b,c,a,d],[b,c,d,a],[b,d,a,c],[b,d,c,a],
    [c,b,a,d],[c,b,d,a],[c,a,b,d],[c,a,d,b],[c,d,b,a],[c,d,a,b],
    [d,b,c,a],[d,b,a,c],[d,c,b,a],[d,c,a,b],[d,a,b,c],[d,a,c,b]])
    for (let o1 in op) for (let o2 in op) for (let o3 in op)
      for (let order in mix=orderMix(x,op[o1],y,op[o2],z,op[o3],w))
        if (Math.abs(mix[order]()-24) < .0001)
          return order.replace(/1/,o1).replace(/2/,o2).replace(/3/,o3).replace(/x/,x).replace(/y/,y).replace(/z/,z).replace(/w/,w)
  return "It's not possible!"
}
