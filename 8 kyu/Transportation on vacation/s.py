568d0dd208ee69389d000016


def rental_car_cost(d):
    result = d * 40
    if d >= 7:
        result -= 50
    elif d >= 3:
        result -= 20
    return result
__________________________
def rental_car_cost(d):
  return d * 40 - (d > 2) * 20 - (d > 6) * 30
__________________________
def rental_car_cost(d):
    discount = 0
    if d >= 7:
        discount = 50
    elif d >= 3:
        discount = 20
    return d * 40 - discount
__________________________
def rental_car_cost(d):
    if d >= 7: return d * 40 - 50
    elif d >= 3: return d * 40 - 20
    return d * 40
__________________________
def rental_car_cost(d):
    return d*40 - 50 if d >= 7 else d*40 -20 if d >= 3 else d*40  
__________________________
def rental_car_cost(d):
    return 40 * d - ((50, 20)[d < 7], 0)[d < 3]
__________________________
def rental_car_cost(d):
    discount = 50 if d > 6 else 20 if d > 2 else 0 
    return d * 40 - discount
__________________________
def rental_car_cost(d):
    return d * 40 - 20 * (d >= 3) - 30 * (d >= 7)
__________________________
def rental_car_cost(d):
    return 40*d - (50 if d >= 7 else 20 if d >= 3 else 0)
__________________________
def rental_car_cost(d):
    total_cost = d * 40
    if d >= 7:
        total_cost -= 50
    elif d >= 3:
        total_cost -= 20
    return total_cost
__________________________
def rental_car_cost(d):
    if d < 3 :
        result = d * 40
    elif d > 2 and d < 7 :
        result = (d * 40) - 20
    else :
        result = (d * 40) - 50
    return result
__________________________
def rental_car_cost(d):
    total = 0
    if d >= 7:
        total = d*40 - 50
    elif d >=3  and d <= 6:
        total = d * 40 - 20
    else:
        total = d * 40
    return total
__________________________
EVERY_DAY_RENT = 40


def rental_car_cost(d):
    rent_total = EVERY_DAY_RENT * d
    if d >= 7:
        rent_price = rent_total - 50
        return rent_price
    if d >= 3:
        rent_price = rent_total - 20
        return rent_price
    else:
        rent_price = rent_total
    return rent_price
__________________________
EVERY_DAY_RENT = 40
DISCOUNT_20_DAYS = 3
DISCOUNT_50_DAYS = 7


def rental_car_cost(d):
    if d >= DISCOUNT_50_DAYS:
        rent_price = EVERY_DAY_RENT * d - 50
        return rent_price
    elif d >= DISCOUNT_20_DAYS:
        rent_price = EVERY_DAY_RENT * d - 20
        return rent_price
    else:
        rent_price = EVERY_DAY_RENT * d
    return rent_price
__________________________
def rental_car_cost(d):
    if d <= 2:
        return d * 40
    elif d>2 and d<7:
        return (d * 40) - 20
    else:
        return (d * 40) - 50
__________________________
def rental_car_cost(d):
    discount_1 = (d >= 3) * 20
    discount_2 = (d >= 7) * (50 - 20)
    daily_cost = 40
    total_cost = 40 * d
    return total_cost - discount_1 - discount_2
