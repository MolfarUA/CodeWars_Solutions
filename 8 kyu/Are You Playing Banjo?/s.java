53af2b8861023f1d88000832


public class Banjo 
{
  public static String areYouPlayingBanjo(String name) 
  {
    if( name.toUpperCase().startsWith("R") )
      return name + " plays banjo";
    else
      return name + " does not play banjo";
  }
}
________________________________
public class Banjo {
  public static String areYouPlayingBanjo(String name) {
      return (name.charAt(0) == 'r' || name.charAt(0) == 'R') ? name + " plays banjo" : name + " does not play banjo";
  }
}
________________________________
public class Banjo {
  public static String areYouPlayingBanjo(String name) {
    return (name.startsWith("R") || name.startsWith("r") ? name + " plays banjo" : name + " does not play banjo");
  }
}
