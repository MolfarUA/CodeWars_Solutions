55225023e1be1ec8bc000390


using System;

public static class Kata
{
  public static string greet(string name)
  {
     return name == "Johnny"? "Hello, my love!" : "Hello, " + name + "!";
  }
}
__________________________________
using System;

public static class Kata
{
  public static string greet(string name)
  {
    if(name == "Johnny")
      return "Hello, my love!";
    return "Hello, " + name + "!";
  }
}
__________________________________
using System;

public static class Kata
{
  public static string greet(string name)
  {
    if(name == "Johnny")
      return "Hello, my love!";
    else
      return "Hello, " + name + "!";
  }
}
__________________________________
using System;

public static class Kata
{
  public static string greet(string name)
  {
      return $"Hello, {name == "Johnny" ? "my love" : name}!";
  }
}
__________________________________
class Kata
{
  public static string greet(string name) => $"Hello, {(name == "Johnny" ? "my love" : name)}!";
}
