5547cc7dcad755e480000004


using System;
using System.Collections.Generic;

public class RemovedNumbers {
  public static List<long[]> removNb(long n) {
  List<long[]> result = new List<long[]>();
  long sumOfSeq = (n%2==0)?((n+1)*(n/2)):(n*((n+1)/2));
  long b;
  for(long a = n/2; a<=n;a++){
    b = (sumOfSeq - a)/(a+1);
    if( (b*a+b+a) == sumOfSeq){
      result.Add(new long[] {a,b});
    }
  }
  return result;
  
  }
}
______________________________
using System.Collections.Generic;
using System.Linq;
using System;
public class RemovedNumbers {
  public static List<long[]> removNb(long n) {
    return Enumerable.Range((int)n/2,(int)n/2) .Where(x=>(double)(n*(n+1)/2-x)/(x+1)%1==0) .Select(x=>new long[]{x,(n*(n+1)/2-x)/(x+1)}) .ToList();
  }
}
______________________________
using System;
using System.Linq;
using System.Collections.Generic;

public class RemovedNumbers {
    public static List<long[]> removNb(long n) {
        List<long[]> res = new List<long[]>();
        long sum = n * (n + 1) / 2;
        for (long a = 1; a <= n; a++)
        {
            double b = (double)(sum - a) / (a + 1);
            if (b % 1 == 0 && b <= n)
                res.Add(new long[] { a, (long)b });
        }
        
        return res.OrderBy(e => e[0]).ToList();
    }
}
