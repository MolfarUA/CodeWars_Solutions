using System;
class Kata
{
    public static int PsionPowerPoints(int level, int score) => level > 0 && score > 10 ? new int[] { 0, 2, 6, 11, 17, 25, 35, 46, 58, 72, 88, 106, 126, 147, 170, 195, 221, 250, 280, 311, 343 }[Math.Min(level, 20)] + ((score - 10) / 2 / 2 * level) : 0;
}
__________________________
using System;
class Kata
{
    private static int[] Points = new []{0, 2, 6, 11, 17, 25, 35, 46, 58, 72, 88, 106, 126, 147, 170, 195, 221, 250, 280, 311, 343};
  
    public static int PsionPowerPoints(int level, int score)
    {
        return level <= 0 || score <= 10 ? 0 : Points[Math.Min(level, 20)] + (score - 10) / 4 * level;
    }
}
__________________________
using System;
class Kata
{
    public static int PsionPowerPoints(int level, int score)
        {
            if (score < 11 || level < 1) { return 0; }

            int[] pointsPerDay = new int[] { 2, 6, 11, 17, 25, 35, 46, 58, 72, 88, 106, 126, 147, 170, 195, 221, 250, 280, 311, 343 };
            int modifier = score == 0 ? 0 : score / 2 - 5;
            int bonusPoints = modifier / 2 * level;
            
            return pointsPerDay[Math.Min(level - 1, 19)] + bonusPoints;
        }
}
__________________________
using System;
using System.Linq;

class Kata
{
    public static int PsionPowerPoints(int level, int score)
    {
        if (level == 0 || score <= 10) { return 0; }
        
        int[] powerPerDay = new int[] { 0, 2, 6, 11, 17, 25, 35, 46, 58, 72, 88, 106, 126, 147, 170, 195, 221, 250, 280, 311, 343 };

        int modifier = (int) Math.Floor((score - 10) / 2.0);
        int bonusPower = modifier / 2 * level;
        //should be: int bonusPower = modifier * level / 2;
        
        return powerPerDay[Math.Min(level, 20)] + bonusPower;
    }
    
}
__________________________
using System;
using System.Linq;
using System.Collections.Generic;
class Kata
{
    public static int PsionPowerPoints(int level, int score)
    {
      if (level == 0 || score < 11) { return 0; }
      List<int> powerIncrement = new List<int> { 0, 2, 6, 11, 17, 25, 35, 46, 58, 72, 88, 106, 126, 147, 170, 195, 221, 250, 280, 311, 343 };
      return (score - 10) / 2 / 2 * level + powerIncrement[level > 20 ? 20 : level];
    }
}
