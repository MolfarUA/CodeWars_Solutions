function parseK (input) {
  const sign = input[0] === '-' ? -1 : 1;
  const number = Number(input.replace(/^-+/, '') || 1);
  return number * sign;
}
function fact (n) {
  return n <= 1 ? 1 : n * fact(n-1);
}
function binomialCoef (n, k) {
  return fact(n) / (fact(k) * fact(n - k));
}
function signOf (n, omitPlus) {
}
function numberOf (n, omitOne) {
}
function formatCoef (n, omitPlus, omitOne) {
  const abs = Math.abs(n);
  const sign = abs / n;
  const signStr = sign < 0 ? '-' : omitPlus ? '' : '+';
  const numStr = abs !== 1 ? abs : omitOne ? '' : 1;
  return `${signStr}${numStr}`;
}
function expand(expr) {
  const parts = /\((?<a>-?\d*)(?<x>[a-z])(?<b>[+-]\d*)\)\^(?<n>\d+)/.exec(expr);
  if (!parts) throw new Error(`Parsing error for ${expr}`);

  const power = parseK(parts.groups.n);
  if (power < 0) throw new Error(`Unexpected power (${power}) in ${expr}`);
  // fast exit
  if (power === 0) return '1';
  if (power === 1) return `${parts.groups.a}${parts.groups.x}${parts.groups.b}`;
  const x = parts.groups.x;
  
  const a = parseK(parts.groups.a);
  
  const b = parseK(parts.groups.b);
  
  let result = '';
  let curPower = power;
  while (curPower >= 0) {
    const binomial = binomialCoef(power, curPower);
    const coef = binomial * Math.pow(a, curPower) * Math.pow(b, power - curPower);
    
    if (!coef) { curPower--; continue; }
    
    const coefStr = formatCoef(coef, curPower === power, curPower);
    const xChar = curPower ? x : '';
    const powerSign = curPower > 1 ? `^${curPower}` : '';
    
    result += `${coefStr}${xChar}${powerSign}`;
    curPower--;
  }
  return result;
}

___________________________________________________
const expand = (expr) => {
  let arr = expr.match(/\((\d+|-\d+|-|)([a-z])(\+|\-)(\d+)\)\^(\d+)/);
  let a = arr[1] === '' ? 1 : arr[1] === '-' ? -1 : +arr[1];
  let x = arr[2];
  let b = arr[3] === '-' ? -arr[4] : +arr[4];
  let n = +arr[5];
  let result = '';

  if(n === 0) return '1';
  if(b === 0) return (a === 1 && result === '' ? '' : a === -1 ? '-' : Math.pow(a, n).toString()).concat(x).concat(`^${n}`);

  const nOverK = (n, k) => {
    //n -> n-k+1
    //k -> n
    let nFac = 1, kFac = 1;
    if(k === 0 || k === n){
      return 1;
    } else if (k === 1 || k === n-1){
      return n;
    } else {
      for(let i = 0; i < k; i++){
        nFac *= (n-i);
        kFac *= (k-i);
      }
    }
    return nFac/kFac;
  }

  for(let k = 0; k <= n; k++){
    let calculation = nOverK(n, k) * Math.pow(a, n-k) * Math.pow(b, k);
    calculation = (calculation === 1 && result === '') ? '' : (calculation === -1 && result === '') ? '-' : calculation.toString();
    let expression = calculation.concat((n-k === 0) ? '' : (n-k === 1 ? `${x}` : `${x}^${n-k}`));
    result += calculation < 0 ? expression : `+${expression}`;
  }
  result = result.replace(/(--)/g, '+').replace(/(\+-)/g, '-');
  return result.charAt(0) === '+' ? result.slice(1) : result;
}

___________________________________________________
function factorial(n) {
  if (n <= 1) {
    return 1
  }
  
  return n * factorial(n-1)
}

function expand(expr) {
  const [base, power] = expr.split("^");

  if (power === "0") {
    return "1";
  } else if (power === "1") {
    return base.slice(1).slice(0, base.length - 2);
  }

  const signs = ["-", "+"];
  const result = [];
  const operands = {
    leftCoeff: "",
    leftVar: "",
    rightCoeff: "",
    rightVar: "",
  };

  let fields = Object.keys(operands);
  let currentField = 0;

  base.split("").forEach((char) => {
    if (char === "(" || char === ")" || char === " ") {
      return;
    }

    if (
      fields[currentField] === "leftCoeff" &&
      !signs.includes(char) &&
      isNaN(char)
    ) {
      currentField = 1;
    } else if (
      fields[currentField] === "leftVar" &&
      (signs.includes(char) || !isNaN(char))
    ) {
      currentField = 2;
    } else if (
      fields[currentField] === "rightCoeff" &&
      !signs.includes(char) &&
      isNaN(char)
    ) {
      currentField = 3;
    }

    operands[fields[currentField]] =
      operands[fields[currentField]].concat(char);
  });

  if (operands.leftCoeff === "-") {
    operands.leftCoeff = "-1";
  } else if (operands.leftCoeff === "") {
    operands.leftCoeff = "1";
  }

  const n = Number(power);
  let k = 0;

  // Some shano checks
  let resultString = "";

  function getCoeff(coeff, k, n) {
     if ((coeff !== -1 && coeff !==1) || n-k === 0){ 
       return coeff
     }
    
    if (k === 0){
      return coeff === -1 ? '-' : ''
    }
    
  }
  
  while (k <= n) {
    console.log({k , n,'n-k': n-k, 'n/k': n/k, left: operands.leftCoeff, right: operands.rightCoeff})
    const coefficient = Math.floor(
      (k === 0 ? 1 : factorial(n) / (factorial(n-k) * factorial(k))) *
        (operands.leftCoeff ** (n - k)) *
        (operands.rightCoeff ** k)
    );

    if (coefficient === 0) {
      k++;
      continue;
    }

    const temp = `${getCoeff(coefficient, k, n)}${
      n - k > 0 ? `${operands.leftVar}${n - k > 1 ? "^" + (n - k) : ""}` : ""
    }`;

    if (!temp.startsWith("-") && k !== 0) {
      resultString += "+" + temp;
    } else {
      resultString += temp;
    }

    k++;
  }

  console.log(expr, resultString);
  return resultString;
}

___________________________________________________
function expand(expr) {

  function isLetter(c) {
    return c.toLowerCase() != c.toUpperCase();
  }

  function coeff(exponent, place) {
    let fact1 = Array.from({
      length: xp
    }, (_, i) => i + 1).reduce(
      (a, b) => a * b
    );
    let fact2 =
      place > 0 ?
      Array.from({
        length: place
      }, (_, i) => i + 1).reduce((a, b) => a * b) :
      1;
    let fact3 = Array.from({
      length: xp - place
    }, (_, i) => i + 1).reduce(
      (a, b) => a * b
    );

    return fact1 / (fact2 * fact3);
  }
  let checkPoint = 1;
  let index = 0;
  let num = [];
  expr.split("").forEach((e, i) => {
    if (isLetter(e)) {
      num[index] = expr.slice(checkPoint, i);
      num[index].length === 0 ? (num[index] = 1) : num[index];
      if (num[index] === "-") {
        num[index] = -1;
      } else {
        num[index] = +num[index];
      }
      num[index + 1] = e;
      checkPoint = i + 1;
      index += 2;
    }
    if (e === ")") {
      num[index] = +expr.slice(checkPoint, i);
      checkPoint = i + 1;
      index += 1;
    }
    if (e === "^") {
      num[index] = +expr.slice(i + 1);
    }
  });


  let x = num[0];
  let y = num[2];
  let xp = num[3];
  let vari = num[1];

  let result = [];
  let xpCount = 0;

  function iterateExp() {
    for (i = 0; i < xp; i++) {
      let mult = coeff(xp, i) * x ** (xp - i) * y ** i;
      if (mult > 0 && i > 0) {
        result.push("+" + mult);
      } else {
        result.push(mult);
      }
      if (mult === 1) {
        result[i] = "";
      }
      if (mult === -1) {
        result[i] = "-";
      }
      xp - i > 0 ? result.push(vari) : null;
      xp - i > 1 ? result.push("^" + (xp - i)) : null;
    }
    let lastMult = y ** xp;
    if (lastMult > 0 && result.length > 1) {
      result.push("+" + lastMult);
    } else if (lastMult < 0 || lastMult === 1) {
      result.push(lastMult);
    }

    return result;
  }

  if (y !== 0) {
    return iterateExp().join("");
  } else {
    console.log("hey")
    return x ** xp !== 1 && x ** xp !== -1 ? x ** xp + vari + "^" + xp : "" + vari + "^" + xp;
  }
}
