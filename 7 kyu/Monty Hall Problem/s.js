function montyHall(correctDoorNumber, participantGuesses) {
  correctDoorNumber = participantGuesses.filter(el => el === correctDoorNumber).length
  participantGuesses = participantGuesses.length
  return 100 - Math.round(100 * correctDoorNumber / participantGuesses)
}
_________________________________________________
function montyHall(correctDoorNumber, participantGuesses) {
  const wins = participantGuesses.filter(guess => guess !== correctDoorNumber).length;
  const winPercentage = Math.round(wins * 100 / participantGuesses.length);
  return winPercentage;
}
_________________________________________________
const montyHall=(c, p) => +(p.reduce((s,n)=> s + ( n-c ? 100 : 0),0)/p.length).toFixed();
