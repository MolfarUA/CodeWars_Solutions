563f037412e5ada593000114


public class Money {
  public static int calculateYears(double principal, double interest, double tax, double desired) {
    int years = 0;
    while (principal < desired) {
      principal += principal * interest * (1 - tax);
      years++;
    }
    return years;
  }
}
_________________________
public class Money {
  public static int calculateYears(double principal, double interest,  double tax, double desired) {            
    return (int) Math.ceil(Math.log(desired / principal) / Math.log(1 + interest * (1 - tax)));
  }
}
_________________________
public class Money {
  public static int calculateYears(double principal, double interest,  double tax, double desired) {
    int years = 0;
    
    while (principal < desired) {
      years++;
      principal += (principal * interest) - (principal * interest * tax);
    }
    
    return years;
  }
}
