595bbea8a930ac0b91000130

function calculate1RM(w, r) {

  if (r <= 1) return r * w;

  let   epley = w * (1 + r / 30)
  , mcglothin = 100 * w / (101.3 - 2.67123 * r)
  ,  lombardi = w * Math.pow(r, 0.1);

  return Math.round(Math.max(epley, mcglothin, lombardi));

}
_______________________________
function calculate1RM(w, r){
  return r == 1 ? w : r == 0 ? 0 : Math.round(Math.max(...["w*(1+r/30)", "(100*w)/(101.3-2.67123*r)", "w*(r**0.10)"].map(a => eval(a))))
}
_______________________________
function calculate1RM (w, r) {
console.log(w)
console.log(r)
  if (r === 1) return w;
  if (r === 0) return 0;
  
  const firstFormula = w * (1 + r / 30);
  const secondFormula = (100 * w) / (101.3 - 2.67123 * r);
  const thirdFormula = w * Math.pow(r, 0.1);
  
//   const maxVal = 1
  const maxVal = Math.max(firstFormula, secondFormula, thirdFormula);
  console.log(maxVal);
  return Math.round(maxVal); 
}
_______________________________
const calculate1RM = (w, r) => {
  if (r == 1) return w;
  if (r == 0) return 0;
  const maxByEpley = Math.round(w * (1 + r / 30));
  const maxByMcGlothin = Math.round((100 * w) / (101.3 - 2.67123 * r));
  const maxByLombardi = Math.round(w * r ** 0.1);
  return Math.max(maxByEpley, maxByMcGlothin, maxByLombardi);
};
_______________________________
function calculate1RM(w, r) {
  if (r === 0) return 0;
  if (r === 1) return w;

  return Math.max(...[Math.round(w * (1 + r / 30)),
    Math.round(100 * w / (101.3 - 2.67123 * r)),
      Math.round(w * r ** 0.10)] );
}
_______________________________
const calculate1RM = (w, r) => r > 1 ? Math.round(Math.max(w * r**0.10, (100 * w) / (101.3 - 2.67123 * r), w * (1 + r / 30))) : w * r
