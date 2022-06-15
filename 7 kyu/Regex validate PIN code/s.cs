using System;
using System.Linq;
using System.Text.RegularExpressions;

public class Kata
{
  public static bool ValidatePin(string pin)
  {
       return pin.All(n => Char.IsDigit(n)) && (pin.Length == 4 || pin.Length == 6);
  }
}
____________________________
using System;
using System.Text.RegularExpressions;

public class Kata
{
  public static bool ValidatePin(string pin)
  {
    return Regex.IsMatch(pin, @"^(\d{6}|\d{4})\z");
  }
}
____________________________
using System;
using System.Text.RegularExpressions;

public class Kata
{
  public static bool ValidatePin(string pin)
  {
    if(pin.Length == 4  || pin.Length == 6) {
      for(var chr=0;chr< pin.Length;chr++){
        if(!Char.IsDigit(pin, chr)){
          return false;
        }
      }
      return true;
    }
    else return false;
  }
}
____________________________
using System;
using System.Text.RegularExpressions;

public class Kata
{
  public static bool ValidatePin(string pin)
  {
    foreach (char c in pin)
    {
       if (!Char.IsDigit(c))
       {
           return false;        
       }
    }
    int tamanhoPin = pin.Length;
    
    if (tamanhoPin == 4 || tamanhoPin == 6)
        return true;
      return false;
  }
}
____________________________
using System;
using System.Text.RegularExpressions;
using System.Linq;

public class Kata
{
  public static bool ValidatePin(string pin)
  {
    return (pin.Length == 4 || pin.Length == 6) && pin.All(char.IsDigit);
  }
}
