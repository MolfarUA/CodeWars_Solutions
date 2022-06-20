5ab6538b379d20ad880000ab


const areaOrPerimeter = (l, w) => (l===w) ? l * w : 2 * (l + w)
###########
const areaOrPerimeter = (l , w) => l === w ? l*w : 2*(l+w);
############
const areaOrPerimeter = function(l , w) {
  return l == w ? l*w : 2*(l + w)
};
###########
const areaOrPerimeter = function(l , w) {
  let area = l * w;
  let perimeter = (l + w) * 2;
  
  return l === w ? area : perimeter;
};
#############
const areaOrPerimeter = (l , w) =>
  l - w ? (l + w) * 2 : l ** 2;
###########
const areaOrPerimeter = function(l , w) {
    const isSquare = l === w ? true : false;
    return isSquare ? l * w : l * 2 + w * 2;
};
############
const areaOrPerimeter = function(l , w) {
  let result = 0;
  l === w ? result = l**2 : result = 2 * (l + w);
  return result;
};
##########
const areaOrPerimeter = function(l , w) {
  if(l === w)
    return l*w;
  else
    return (2*l)+(w*2);
};
#########
