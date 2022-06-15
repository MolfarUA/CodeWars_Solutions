using System.Linq;
using System;
public static class Kata 
{
  public static bool XO (string input)
  {
     return input.ToLower().Count(i => i == 'x') == input.ToLower().Count(i => i == 'o');
  }
}
__________________________________
using System.Linq;
using System;
public static class Kata 
{
  public static bool XO (string input)
  {
    int x = 0;
    int o = 0;

    foreach (var c in input)
    {
        if (c.ToString().ToUpper() == "X")
        {
            x++;
        }
        else if (c.ToString().ToUpper() == "O")
        {
            o++;
        }
    }

    if (x == o || x == 0 && o == 0)
    {
        return true; 
    }
    else
    {
        return false;
    }
  }
}
__________________________________
using System.Linq;
using System;
public static class Kata 
{
  public static bool XO (string input)
  {
    char[] s= input.ToCharArray();
    int x=0;
    int o=0;
    
    foreach(char c in s)
    {
      if(c=='x'||c=='X')
      {
        x++;
      }
      else if(c=='o'||c=='O')
      {
        o++;
      }
    }
    
    if(x==o)
    {
      return true;
    }
    else
    {
      return false;
    }
  }
}
__________________________________
using System.Linq;
using System;
public static class Kata 
{
  public static bool XO (string input)
  {
    int i = 0;
    foreach (char c in input){
      if (char.ToUpperInvariant(c) == 'X') i++;
      else if (char.ToUpperInvariant(c) == 'O') i--;
    }
    return i == 0;
  }
}
__________________________________
using System.Linq;
using System;
public static class Kata 
{
  public static bool XO (string input)
  {
    input = input.ToLower();
    int amountOfX = 0;
    int amountOfO = 0;
    bool result = true;
    for(int i=0; i<input.Length;i++){
      
      if(input[i] == 'x'){
        amountOfX++;
      }
      if(input[i] == 'o'){
        amountOfO++;
      }
    }
    if(amountOfX!=amountOfO){
      result = false;
    }
    return result;
  }
}
__________________________________
using System.Linq;
using System;
public static class Kata 
{
  public static bool XO (string input)
  {
    int oAmount = 0, xAmount = 0;
    foreach (char c in input.ToLower())
    {
      if (c == 'o')
      {
        oAmount++;
      }
      else if (c == 'x')
      {
        xAmount++;
      }
    }
    return xAmount == oAmount;
  }
}
__________________________________
using System.Linq;
using System;
public static class Kata 
{
  public static bool XO (string input)
  {
    int numberX = 0;
    int numberY = 0;

    foreach(char letter in input)
    {
      if(letter == 'x'|| letter == 'X')
        numberX++;
      else if(letter == 'o'|| letter == 'O')
        numberY++;
    }
    
    return numberX == numberY;
  }
}
