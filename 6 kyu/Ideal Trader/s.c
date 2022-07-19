610ab162bd1be70025d72261


#include <stddef.h>

double ideal_trader(const double* prices, size_t n_prices)
{
    
  if (n_prices <= 1) return 0;
  double result = 1;
  double temp = prices[0];
  for (size_t i = 1; i < n_prices; i++){
    if (prices[i] > temp)
      {
      result += result*(prices[i]-temp)/temp;      
    }
    temp =  prices[i];
  }
    return result;
}
__________________________________
#include <stddef.h>

double ideal_trader(const double* prices, size_t n_prices)
{
  double result = 1.0;
  for(size_t i = 1; i < n_prices; i++)
  {
    if(prices[i] > prices[i - 1])
    {
      result *= prices[i] / prices[i - 1];
    }
  }
  return result;
}
__________________________________
#include <stddef.h>

double ideal_trader(const double* prices, size_t n_prices)
{
    double deposit = 1, amount = 0;
  
    for (size_t i = 0; i < n_prices; ++i) {
        if (amount == 0 && i + 1 < n_prices && prices[i] < prices[i + 1]) {
            amount = deposit/prices[i];
            deposit = 0;
        }
        if (deposit == 0 && (i + 1 == n_prices || prices[i] > prices[i + 1])) {
            deposit = amount*prices[i];
            amount = 0;
        }
    }
  
    return deposit;
}
