56f6ad906b88de513f000d96


public class Kata{
  public static String bonusTime(final int salary, final boolean bonus) {
    return "\u00A3" + (bonus ? 10 : 1) * salary;
  }
}
__________________________
public class Kata{
   public static String bonusTime(final int salary, final boolean bonus)
   {
      return "£" + salary * (bonus ? 10 : 1);
   }
}
__________________________
public class Kata{
  public static String bonusTime(final int salary, final boolean bonus) {
    return (bonus)?new String("\u00A3"+salary*10):new String("\u00A3"+salary);
  }
}
