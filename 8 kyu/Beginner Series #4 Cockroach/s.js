55fab1ffda3e2e44f00000c6


const cockroachSpeed = s => Math.floor(s / 0.036);
__________________________
function cockroachSpeed(s) {
  const secsInHour = 3600;
  const centimetersInKilometers = 100000;
  
  return Math.floor((s*centimetersInKilometers)/secsInHour);
}
__________________________
function cockroachSpeed(s) {
  return Math.floor(s*100000/3600);
}
__________________________
function cockroachSpeed(s) {
  const KILOMETER_IN_CENTIMETERS = 1 * 1000 * 100;
  const HOUR_IN_SECONDS = 1 * 60 * 60;
  
  return Math.floor(s * KILOMETER_IN_CENTIMETERS / HOUR_IN_SECONDS);
}
__________________________
const cockroachSpeed = s => 
  s / 3.6e-2 ^ 0;
__________________________
const cockroachSpeed = s => s/.036|0
