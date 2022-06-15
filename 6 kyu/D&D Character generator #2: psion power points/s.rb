def psion_power_points(level,score)
  return 0 if level.zero? || score <= 10
  
  power_points = [0, 2, 6, 11, 17, 25, 35, 46, 58, 72, 88, 
    106, 126, 147, 170, 195, 221, 250, 280, 311, 343]
  
  power_point = level <= 20 ? power_points[level] : 343
  
  n = (score - 10) / 2
  
  bonus_point = if level.even? 
                  level / 2 * n
                else
                  level / 2 * n + (n/2)
                end
  power_point + bonus_point
end
__________________________
$points = [0, 2, 6, 11, 17, 25, 35, 46, 58, 72, 88, 106, 126, 147, 170, 195, 221, 250, 280, 311, 343];

def psion_power_points(level,score)
  level <= 0 || score <= 10 ? 0 : $points[[level, 20].min] + (score - 10) / 2 * level / 2
end
__________________________
$power_points_per_day = [2, 6, 11, 17, 25, 35, 46, 58, 72, 88, 106, 126, 147, 170, 195, 221, 250, 280, 311, 343]

def psion_power_points(level, score)
  return 0 unless score > 10 && level.positive?
  
  lvl = [20, level].min
  modifier = (score - 10) / 2
  
  $power_points_per_day[lvl - 1] + (level * modifier * 0.5).floor
end
__________________________
def psion_power_points(l,s) l>0 && s>10 ? [0,2,6,11,17,25,35,46,58,72,88,106,126,147,170,195,221,250,280,311,343][[l,20].min]+(s-10)/2*l/2 : 0 end
