568d0dd208ee69389d000016


def rental_car_cost(d)
  return d * 40 if d < 3
  return d * 40 - 20 if d < 7
  return d * 40 - 50
end
__________________________
def rental_car_cost(days)
  discount = 0
  discount = 20 if days >= 3
  discount = 50 if days >= 7
  days * 40 - discount
end
__________________________
def rental_car_cost(d)
    r=d*40
    d<3 ? r : (d<7 ? r-20 : r-50)
end
