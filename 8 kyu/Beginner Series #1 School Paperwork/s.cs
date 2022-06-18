55f9b48403f6b87a7c0000bd


  using System;
  public static class Paper
  {
    public static int Paperwork(int n, int m) => (n > 0 && m > 0) ? m*n : 0;
  }
__________________________
  using System;
  public static class Paper
  {
    public static int Paperwork(int n, int m)
    {
      if (n < 0) n = 0;
      if (m < 0) m = 0;
      
      return n*m;
    }
  }
__________________________
  using System;
  public static class Paper
  {
    public static int Paperwork(int n, int m) => n > 0 && m > 0 ? n * m : 0;
  }
__________________________
  using System;
  public static class Paper
  {
    public static int Paperwork(int n, int m)
     => Math.Max(n,0) * Math.Max(m, 0);
  }
__________________________
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
 
public static class Paper
{
  public static int Paperwork(int n, int m)
  {
     return (m > 0) && (n > 0) ? (n * m) : 0;
  }
}
