56f6ad906b88de513f000d96


bonusTime = (salary, bonus) ->
  if bonus
    '£' + salary * 10
  else
    '£' + salary
__________________________
bonusTime = ( s,b ) -> '£' + if b then s*10 else s
__________________________
bonusTime = ( salary,bonus ) -> if bonus then "£#{10*salary}" else "£#{salary}"
