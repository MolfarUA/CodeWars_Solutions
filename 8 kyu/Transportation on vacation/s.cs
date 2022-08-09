568d0dd208ee69389d000016


public class RentalCar {
   
   public static int RentalCarCost(int d) {
       // your code
       int totalAmount = d * 40;
       if (d>6) {
         totalAmount = totalAmount - 50;
         }
       else if (d>2) {
         totalAmount = totalAmount - 20;
         }
       
       return totalAmount;
       
   }
}
__________________________
using System;
public class RentalCar {
    
    public static int RentalCarCost(int d) {
        return d*40-(d>6?50:d>2?20:0);
    }
}
__________________________
public class RentalCar
{    
    public static int RentalCarCost(int d)
    {
        return d >= 7 ? d * 40 - 50 : d >= 3 ? d * 40 - 20 : d * 40;
    }
}
__________________________
public class RentalCar {
    
    public static int RentalCarCost(int d) 
    {
        int dailyRate = 40;
        int threeDayDiscount = 20;
        int weeklyDiscount = 50;
        
        int calculatedCost = 0;
        
        calculatedCost = d * dailyRate;
        
        if ( (d >= 3) && (d <=6) )
          calculatedCost = calculatedCost - threeDayDiscount;
          
        if (d >= 7)
          calculatedCost = calculatedCost - weeklyDiscount;  
        
        return calculatedCost;
    }
}
