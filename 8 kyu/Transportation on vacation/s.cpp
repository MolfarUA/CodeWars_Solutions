568d0dd208ee69389d000016
  
  
int rental_car_cost(int d){
  return d >= 7? d * 40 - 50:  d >= 3? d * 40 - 20: d * 40;
}
__________________________
int rental_car_cost(int d){
  int total = d * 40;
  if (d >= 7)
    return total - 50;
  else if (d >= 3)
    return total - 20;
  return total;
}
__________________________
int rental_car_cost(int d){
  int perDay = 40;
  int discount = 0;
  int total = perDay * d;
  
  if (d >= 7) discount = 50;
  else if (d >= 3) discount = 20;
  
  if (total - discount >= perDay) total -= discount;
  else total = perDay;
  return total;
}
