psion_power_points=lambda l,s: [0,2,6,11,17,25,35,46,58,72,88,106,126,147,170,195,221,250,280,311,343][min(l,20)]+(s-10)//2*l//2 if l and s>10 else 0
__________________________
powers = [0,2,6,11,17,25,35,46,58,72,88,106,126,147,170,195,221,250,280,311,343]
def psion_power_points(level, score):
    score = max(score - 10, 0)
    return level * score and score // 2 * level // 2 + powers[min(level, 20)]
__________________________
def psion_power_points(level,score):
    if not level or score<=10 : return 0
    base=[2,6,11,17,25,35,46,58,72,88,106,126,147,170,195,221,250,280,311,343][min(level,20)-1]
    bonus=(score-10)//4+(((score-10)//2)*(level-1)+1)//2
    return base+bonus
__________________________
lv = {
    0: 0,
    1: 2,
    2: 6,
    3: 11,
    4: 17,
    5: 25,
    6: 35,
    7: 46,
    8: 58,
    9: 72,
    10: 88,
    11: 106,
    12: 126,
    13: 147,
    14: 170,
    15: 195,
    16: 221,
    17: 250,
    18: 280,
    19: 311,
    20: 343,
}


def psion_power_points(l, v):
    if v <= 10: return 0
    return int(max(0, (v - 10) // 2) * 0.5 * l) + lv[min(20, l)]
__________________________
lst=[0,2,6,11,17,25,35,46,58,72,88,106,126,147,170,195,221,250,280,311,343]

psion_power_points=lambda l,s: lst[min(l,20)]+(s-10)//2*l//2 if l and s>10 else 0
__________________________
P = [0, 2, 6, 11, 17, 25, 35, 46, 58, 72, 88, 106, 126, 147, 170, 195, 221, 250, 280, 311, 343];

def psion_power_points(level,score):
    if level <= 0 or score <= 10: return 0
    return P[min(level, 20)] + int((score - 10 >> 1) * (level / 2))
__________________________
ppd = [2, 6, 11, 17, 25, 35, 46, 58, 72, 88, 106, 126, 147, 170, 195, 221, 250, 280, 311, 343]
def psion_power_points(level,score):
    return 0 if score <= 10 or level < 1 else ppd[min(20, level) - 1] + (0 if score < 12 else (score - 10) // 4 * level + (score - 10) % 4 // 2 * level // 2)
__________________________
power={1:2, 2:6, 3:11, 4:17, 5:25, 6:35, 7:46, 8:58, 9:72, 10:88,
       11:106, 12:126, 13:147, 14:170, 15:195, 16:221,
       17:250, 18:280, 19:311, 20:343}
def psion_power_points(level,score):
    if level==0 or score<=10:
        return 0
    return power.get(level,343)+level*((score-score%2)-10)//4
__________________________
inc = {1:2,2:6,3:11,4:17,5:25,6:35,7:46,8:58,9:72,10:88,11:106,12:126,13:147,14:170,15:195,16:221,17:250,18:280,19:311,20:343}

def psion_power_points(level,score):
    
    if level > 0 and score > 10:
        base_points = inc.get(level,343)        
    else:
        base_points = 0   
    
    bonus_points = max(0,int((score - 10) // 2 * 0.5 * level))
    
    return base_points + bonus_points #if score > 11 else base_points
__________________________
import math
def psion_power_points(level,score):
    day = [ 0,2,6,11,17,25,35,46,58,72,88,106,126,147,170,195,221,250,280,311,343]
    return  math.floor(level * (score//2-5) * 0.5) + ( day[level] if level <20 else 343) if score >10 else 0
__________________________
def psion_power_points(level,score):
    power_list = [0, 2, 6, 11, 17, 25, 35, 46, 58, 72, 88, 106, 126, 147, 170, 195, 221, 250, 280, 311, 343]
    if level < 1 or score < 11:
        return 0
    else:
        bonus = int((score-10)//2*0.5*level)
        base_points = power_list[level] if level <= 20 else power_list[20]
        return bonus + base_points
__________________________
powerPointsPerDay = [0,   2,   6,  11,  17,  25,  35,  46,  58,  72,  88,
                        106, 126, 147, 170, 195, 221, 250, 280, 311, 343]
def psion_power_points(level, score):
    # pppd: Power points per day
    # bpp: Bonus power points
    if score <= 10:
        return 0
    pppd = powerPointsPerDay[min(level, 20)]
    bpp = (score - 10) // 2 * level // 2
    return pppd + bpp
