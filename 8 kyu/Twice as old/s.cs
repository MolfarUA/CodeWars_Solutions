5b853229cfde412a470000d0


using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Solution
{
  public class TwiceAsOldSolution
  {
    public static int TwiceAsOld(int dadYears, int sonYears)
    {
      return Math.Abs(dadYears - sonYears * 2);
    }
  }
}
______________________________
using System;

namespace Solution
{
  public class TwiceAsOldSolution
  {
    public static int TwiceAsOld(int dadYears, int sonYears)
    {
      return Math.Abs(dadYears - sonYears * 2);
    }
  }
}
______________________________
using System;
namespace Solution
{
  public class TwiceAsOldSolution
  {
    public static int TwiceAsOld(int dadYears, int sonYears) => Math.Abs(dadYears - (sonYears * 2));
  }
}
______________________________
using System;
namespace Solution
{
  public class TwiceAsOldSolution
  {
      public static int TwiceAsOld(int dadYears, int sonYears) => Math.Abs(2 * sonYears - dadYears);
  }
}
______________________________
namespace Solution
{
  public class TwiceAsOldSolution
  {
    public static int TwiceAsOld(int dadYears, int sonYears)
    {
         int x_year = 2 * sonYears - dadYears;

         if (x_year < 0)
            x_year -= x_year * 2;
            
         return x_year;
    }
  }
}
