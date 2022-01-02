using System;
using System.Collections.Generic;
using System.Linq;

public class Kata
{
  public static int Number(List<int[]> peopleListInOut)
  {
    return peopleListInOut.Sum(Item => Item[0] - Item[1]);
  }
}
_____________________________________
using System;
using System.Collections.Generic;

public class Kata
    {
        public static int Number(List<int[]> peopleListInOut)
        {
            int finalCount = 0;
            for (int i = 0; i < peopleListInOut.Count; i++)
            {
                finalCount += peopleListInOut[i][0];
                finalCount -= peopleListInOut[i][1];
            }
            return finalCount;
        }
    }
_____________________________________
using System;
using System.Collections.Generic;
public class Kata {
  public static int Number(List<int[]> stops) {
    int res = 0;
    foreach(int[] onOff in stops) res += onOff[0] - onOff[1];
    return res;
  }
}
