55cb632c1a5d7b3ad0000145


public class Kata
{
  public static string HoopCount(int n)
  {
    return n<10?"Keep at it until you get it":"Great, now move on to tricks";
  }
}
_____________________________
public class Kata
{
  public static string HoopCount(int n)
  {
    return (n > 9) ? "Great, now move on to tricks" : "Keep at it until you get it";
  }
}
_____________________________
public class Kata
{
  public static string HoopCount(int n)
  {
    const int HOPS_LIMIT = 10;
    return n >= HOPS_LIMIT
      ? "Great, now move on to tricks"
      : "Keep at it until you get it";
  }
}
_____________________________
public class Kata
{
  private const string YoureAwesome = "Great, now move on to tricks";
        private const string Encourage = "Keep at it until you get it";

        public static string HoopCount(int n)
        {
            return n >= 10 ? YoureAwesome : Encourage;
        }
}
