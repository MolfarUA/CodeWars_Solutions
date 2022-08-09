568d0dd208ee69389d000016


unsigned rental_car_cost(unsigned d) {
  return (d >= 7) ? (d*40)-50 : d >= 3 ? (d*40)-20 : d*40;
}
__________________________
unsigned rental_car_cost(unsigned d)
{
  int x = 40;
   
  switch (d) {
    
    case 0: case 1: case 2:
    return d * x;
    
    case 3: case 4: case 5: case 6:
    return (x * d) - 20;    
  
    default: return (x * d) - 50;
  }
}
__________________________
unsigned rental_car_cost(unsigned d)
{
  unsigned rebate = 0;
  if (d > 6)
  {
    rebate = 50;
  }
  else if (d > 2)
  {
    rebate = 20;
  }
  return (d * 40u) - rebate;
}
__________________________
unsigned rental_car_cost(unsigned d)
{
    return (d * 40) - (d >= 7 ? 50 : d >= 3 ? 20 : 0);
}
__________________________
unsigned rental_car_cost(unsigned d)
{
    unsigned m = d * 40;
    if (d > 2) m -= 20;
    if (d > 6) m -= 30;
    return m;
}
__________________________
#define RENT_COST 40
#define BIG_DISCOUNT 50
#define SMALL_DISCOUNT 20
#define DAYS_FOR_BIG_DISCOUNT 7
#define DAYS_FOR_SMALL_DISCOUNT 3

/* d - the days to rent */
unsigned rental_car_cost(unsigned d)
{
    if (d >= DAYS_FOR_BIG_DISCOUNT)
        return d * RENT_COST - BIG_DISCOUNT;
    if (d >= DAYS_FOR_SMALL_DISCOUNT)
        return d * RENT_COST - SMALL_DISCOUNT;
    return d * RENT_COST;
}
