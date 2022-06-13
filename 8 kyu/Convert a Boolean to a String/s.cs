using System;

public class kata
{
  public static string boolean_to_string(bool b)
  {
  return b.ToString();
  }
}
_________________________________
using System;

public class kata
{
  public static string boolean_to_string(bool b)
  {
     return b?"True":"False";
  }
}
_________________________________
using System;

public class kata
{
  public static string boolean_to_string(bool b)
  {
      if(b) {
        return Boolean.TrueString;
      }
    return Boolean.FalseString;
  }
}
_________________________________
using System;

public class kata
{
  public static string boolean_to_string(bool b)
  {
    if (!b)
      {
      return "False";
    } return "True";
    
  
  }
}
_________________________________
using System;

public class kata
{
  public static string boolean_to_string(bool b)
  {
  string str;
    str = Convert.ToString(b);
    return str;
  }
}
