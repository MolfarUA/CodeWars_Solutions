public class Kata
{
  public static string SayHello(string[] name, string city, string state) =>
    $"Hello, {string.Join(" ", name)}! Welcome to {city}, {state}!";
}
_______________________________________
using System;

public class Kata
{
  public static string SayHello(string[] name, string city, string state)
  { 
    return $"Hello, {String.Join(" ", name)}! Welcome to {city}, {state}!";
  }
}
_______________________________________
using System.Linq;

public class Kata
{
    public static string SayHello(string[] name, string city, string state)
    {
      return $"Hello, {name.Aggregate((a,b) => $"{a} {b}")}! Welcome to {city}, {state}!";
    }
}
_______________________________________
public class Kata
{
  public static string SayHello(string[] name, string city, string state)
  {

            string NAME = string.Join(" ", name);
            string end = $"Hello, {NAME}! Welcome to {city}, {state}!";
            return end;
  }
}
_______________________________________
public class Kata
    {
        public static string SayHello(string[] name, string city, string state)
        {
            string sum= "";
            for(int i = 0; i < name.Length; i++)
            {
                sum = string.Concat(sum," ", name[i]);
            }

            string StringTest = $"Hello,{sum}! Welcome to {city}, {state}!";
            return StringTest;
        }
    }
