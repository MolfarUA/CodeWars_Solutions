55466989aeecab5aac00003e


using System.Collections.Generic;

public class SqInRect
{
    public static List<int> sqInRect(int lng, int wdth)
    {
        if(lng == wdth) return null;
        var squares = new List<int>();
        while (lng > 0 && wdth > 0)
        {
            if (lng < wdth)
            {
                squares.Add(lng);
                wdth -= lng;
            }
            else
            {
                squares.Add(wdth);
                lng -= wdth;
            }
        }
        return squares;
    }
}
______________________________
using System;
using System.Collections.Generic;
public class SqInRect {
  
   public static List<int> sqInRect(int lng, int wdth)
        {
            List<int> res= new List<int>();
            if (lng == wdth || (wdth == 0 || lng == 0))
                return null;

            while (lng != wdth)
            {
                if (lng < wdth)
                {
                    var temp = lng;
                    lng = wdth;
                    wdth = temp;
                }
                lng = lng - wdth;
                res.Add(wdth);

            }
            res.Add(wdth);
            return res;
        }
}
______________________________
using System;
using System.Collections.Generic;

public class SqInRect {
  
  public static List<int> sqInRect(int lng, int wdth) {
    if ( lng == wdth ) return null;
    List<int> list = new List<int>();
    while ( lng > 0 && wdth > 0 ) {
      int max = Math.Max( lng, wdth );
      int min = Math.Min( lng, wdth );
      list.Add(min);
      wdth = min;
      lng = max- min;
    }
    return list;
  }
}
