5786f8404c4709148f0006bf


using System;

class PoleVault
{
  public static double StartingMark(double bodyHeight)
  {
    return Math.Round((3.93548 * bodyHeight + 10.67 - 3.93548 * 1.83) * 100) / 100;
  }
}
____________________________________
using System;

class PoleVault
{
    public static double StartingMark(double bodyHeight) => Math.Round(1.22/ 0.31 * bodyHeight + 9.45 - (1.52 * 1.22 /0.31 ),2);
}
____________________________________
using System;

class PoleVault
{
    public static double StartingMark(double bodyHeight)
    {
      var heightVariation = 1.83-1.52;
      var markVariation = 10.67-9.45;
      double initialHeight = 1.52;
      double initialMark = 9.45;
      var markPerHeight =  markVariation/heightVariation;
      
      return Math.Round(initialMark+(bodyHeight-initialHeight)*markPerHeight,2);
    
    }
}
____________________________________
using System;

class PoleVault
{
    public static double StartingMark(double bodyHeight)
    {
        double delta = (11.85-8.27)/(2.13-1.22);
        return Math.Round(11.85 - (2.13-bodyHeight)*delta,2);
    }
}
