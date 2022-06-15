def psion_power_points(level, score)
  points = [0, 2, 6, 11, 17, 25, 35, 46, 58, 72, 88, 106, 126, 147, 170, 195, 221, 250, 280, 311, 343];
  level <= 0 || score <= 10 ? 0 : points[[20, level].min] + ((score - 10) / 2 * (level / 2.0)).to_i
end
__________________________
def psion_power_points(l,s) l>0 && s>10 ? [0,2,6,11,17,25,35,46,58,72,88,106,126,147,170,195,221,250,280,311,343][[l,20].min]+(s-10) / 2*l / 2 : 0 end
