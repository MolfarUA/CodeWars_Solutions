5b609ebc8f47bd595e000627


function solution([m1,m2,d],[um1,um2,ud]) {
  const G = 6.67e-11 ;
  const conversion = { kg:1, g:1e-3, mg:1e-6, μg:1e-9, lb:.453592
                     , m:1, cm:1e-2, mm:1e-3, μm:1e-6, ft:.3048
                     } ;
  return G * m1 * conversion[um1] * m2 * conversion[um2] / ( d * conversion[ud] ) ** 2 ;
}
____________________________________
const solution = ([m1, m2, r], [um1, um2, ud]) => {
  const G = 6.67e-11;
  const conversion = {kg:1, g:1e-3, mg:1e-6, μg:1e-9, lb:.453592, m:1, cm:1e-2, mm:1e-3, μm:1e-6, ft:.3048};
  return G * m1 * conversion[um1] * m2 * conversion[um2] / ( r * conversion[ud] ) ** 2 ;
}
____________________________________
const G = 6.67e-11;

const values = {
  'μg' : 1e-9,
  'mg' : 1e-6,
  'g'  : 1e-3,
  'lb' : 0.453592,
  'kg' : 1,
  'μm' : 1e-6,
  'mm' : 1e-3,
  'cm' : 1e-2,
  'ft' : 0.3048,
  'm'  : 1
};

solution = (arr_val, arr_unit) =>{

  let m = arr_val[0] * values[arr_unit[0]] * arr_val[1] * values[arr_unit[1]];
  let r = (arr_val[2] * values[arr_unit[2]])**2;
  
  return G * (m / r);
  }
