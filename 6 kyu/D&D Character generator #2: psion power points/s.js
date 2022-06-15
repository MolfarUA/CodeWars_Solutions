const pointsPerDay = [2, 6, 11, 17, 25, 35, 46, 58, 72, 88, 106, 126, 147, 170, 195, 221, 250, 280, 311, 343]

function psionPowerPoints(level, score){
  if (score < 11 || level == 0) return 0
  let modifier = Math.floor((score - 10) / 2), f = parseInt(level * modifier * 0.5), lvl = Math.min(20, level)
  return pointsPerDay[lvl - 1] + f  
}
__________________________
const psionPowerPoints=(l,s)=>l&&s>10?[0,2,6,11,17,25,35,46,58,72,88,106,126,147,170,195,221,250,280,311,343][Math.min(l,20)]+~~(~~((s-10)/2)/2*l):0;
__________________________
function psionPowerPoints(level,score){
  return score<11?0:Math.max(0,[0,2,6,11,17,25,35,46,58,72,88,106,126,147,170,195,221,250,280,311,343][Math.min(level,20)]+((score-10)/2|0)/2*level|0)
}
__________________________
const pp = [0, 2, 6, 11, 17, 25, 35, 46, 58, 72, 88, 106, 126, 147, 170, 195, 221, 250, 280, 311, 343];

function psionPowerPoints(level, score) {
  if (level <= 0 || score <= 10) return 0;
  return pp[Math.min(level, 20)] + (score - 10 >> 1) * (level / 2) | 0;
}
__________________________
function psionPowerPoints(level,score){
  var psionPp = [0,2,6,11,17,25,35,46,58,72,88,106,126,147,170,195,221,250,280,311,343];
  if (score < 11 || level < 1)
    return 0;
  if (level <= psionPp.length-1){
    var classPP = psionPp[level];
  }else{
    var classPP = psionPp[psionPp.length-1];
  }
  var scoreBonus = Math.floor((score - 10) / 2);
  var bonusPP = Math.floor(scoreBonus * level / 2);
  return classPP + bonusPP;
}
