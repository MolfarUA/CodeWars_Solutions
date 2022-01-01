using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;

public class ListFilterer
{
   public static IEnumerable<int> GetIntegersFromList(List<object> listOfItems)
   {
      return listOfItems.OfType<int>(); 
   }
}

_____________________________________________
using System.Collections;
using System.Collections.Generic;
using System.Linq;

public class ListFilterer
{
  public static IEnumerable<int> GetIntegersFromList(List<object> listOfItems)
  {
    return listOfItems.OfType<int>().Cast<int>();
  }
}

_____________________________________________
using System.Collections;
using System.Collections.Generic;

public class ListFilterer
{
   public static IEnumerable<int> GetIntegersFromList(List<object> listOfItems)
   {
      List<int> results = new List<int>();
      
      foreach(var item in listOfItems)
      {
        if(item is int)
        {
          results.Add((int)item);
        }
      }
      
      return results;
   }
}

_____________________________________________
using System.Collections.Generic;
using System.Linq;

public class ListFilterer
{
   public static IEnumerable<int> GetIntegersFromList(List<object> listOfItems)
     => listOfItems.OfType<int>();
}

_____________________________________________
using System.Collections;
using System.Collections.Generic;

public class ListFilterer
{
   public static IEnumerable<int> GetIntegersFromList(List<object> listOfItems)
   {
       foreach (object x in listOfItems)
           if (x is int) yield return (int) x;
   }
}
