def excluding_vat_price(price):
    return round(price / 1.15, 2) if price else -1
##########
def excluding_vat_price(price):
    try:
        return round(price / 1.15, 2)
    except TypeError:
        return -1
##########
excluding_vat_price = lambda p: round(p/115*100, 2) if p else -1
#########
def excluding_vat_price(price):
    return -1 if price is None else round(price/1.15,2)
########
def excluding_vat_price(price):
    try:
        result = price / 1.15
        result = round(result, 2)
        return result
    except TypeError:
        return -1
#########
def excluding_vat_price(price):
    if price:
        return round(price - (price / 1.15) * .15, 2)
    else:
        return -1
##########
excluding_vat_price=lambda _:_ and round(_/1.15,2) or -1
#######
def excluding_vat_price(price):
    if price is None or price <= 0:
        return -1
    return round(price / 1.15, 2)
#########
def excluding_vat_price(price):
    if price == None:
        return -1
    else:
        bef_vat = price / 1.15
        return (round(bef_vat, 2))
###########
def excluding_vat_price(price=0):
    try:
        return round(price*100/115,2)
    except:
        return -1
