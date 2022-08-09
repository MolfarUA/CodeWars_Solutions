568d0dd208ee69389d000016


public class Kata {
  private static final int COST_PER_DAY = 40;
  
  public static int rentalCarCost(int d) {
    if (d < 3)       return d * COST_PER_DAY;
    else if (d >= 7) return d * COST_PER_DAY - 50;
    else             return d * COST_PER_DAY - 20;
  }
}
__________________________
public class Kata {
  private static final int COST_PER_DAY = 40;
  private static final int SMALL_DISCOUNT_DAY_BOUNDARY = 2;
  private static final int BIG_DISCOUNT_DAY_BOUNDARY = 6;
  private static final int SEVEN_DAYS_PLUS_DISCOUNT = 50;
  private static final int THREE_DAYS_PLUS_DISCOUNT = 20;

  public static int rentalCarCost(int d) {
    return carCostsPerDays(d) - discountForDays(d);
  }
  
  private static int carCostsPerDays(int days) {
    return days * COST_PER_DAY;
  }
  
  private static int discountForDays(int days) {
    int discount = 0;
    if (days > BIG_DISCOUNT_DAY_BOUNDARY)
      discount = SEVEN_DAYS_PLUS_DISCOUNT;
    else if (days > SMALL_DISCOUNT_DAY_BOUNDARY)
      discount = THREE_DAYS_PLUS_DISCOUNT;
    return discount;      
  }
}
__________________________
public class Kata {
  public static int rentalCarCost(int d) {
    return d < 7 ? d < 3 ? 40 * d : 40 * d - 20 : 40 * d - 50;
  }
}
