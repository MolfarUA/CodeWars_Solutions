610ab162bd1be70025d72261
  
  
#include <vector>

double ideal_trader(const std::vector<double>& prices)
{
  double coef = 1;
  for (size_t i = 0; i < prices.size()-1; i++){
    if (prices[i+1] > prices[i])
      coef *= prices[i+1] / prices[i];
  }
  return coef;
}
__________________________________
#include <vector>

double ideal_trader(const std::vector<double>& prices)
{
    double priceMultiplier = 1;
  
    auto it = prices.begin();
    double lastPrice = *it++;
    for (; it != prices.end(); it++) {
        double currentPrice = *it;
        if (currentPrice > lastPrice)
            priceMultiplier *= currentPrice / lastPrice;
        lastPrice = currentPrice;
    }
  
    return priceMultiplier;
}
__________________________________
#include <vector>

double ideal_trader(const std::vector<double>& prices)
{
    double result = 1;
    auto prev = prices[0];
  
    for (auto price : prices) {
        if (prev < price) {
            result *= price / prev;
        }
        prev = price;
    }
  
    return result;
}
