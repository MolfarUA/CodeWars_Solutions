568d0dd208ee69389d000016


function baseCost(days, rate) {
  return days * rate;
}

function discountRate(days) {
  if ( days >= 7 ) {
    return 50;
  }
  else if ( days >= 3 ) {
    return 20;
  }
  else {
    return 0;
  }
}

function rentalCarCost(days) {
  return baseCost(days, 40) - discountRate(days);
}
__________________________
const rentalCarCost = d => d * 40 - ((d > 6) ? 50 : ((d > 2) ? 20 : 0));
__________________________
function rentalCarCost(d) {
  return d * 40 - (d >= 7 ? 50 : (d >= 3 ? 20 : 0));
}
