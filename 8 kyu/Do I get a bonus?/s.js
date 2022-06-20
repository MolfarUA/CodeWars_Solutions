56f6ad906b88de513f000d96



function bonusTime(salary, bonus) {
  return bonus ? `£${10 * salary}` : `£${salary}`;
}
__________________________
const bonusTime = (salary, bonus) => `£${salary * (bonus ? 10 : 1)}`;
__________________________
function bonusTime(salary, bonus) {
  return '£' + salary * (bonus ? 10 : 1);
}
