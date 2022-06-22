563f037412e5ada593000114


def calculate_years(principal, interest, tax, desired)
  year = 0
  while principal < desired
    year += 1
    income = principal * interest
    principal += income - income * tax
  end
  year
end
_________________________
def calculate_years(principal, interest, tax, desired)
  return 0 if principal >= desired      
  Math::log(desired.to_f / principal, 1 + interest * (1 - tax)).ceil
end
_________________________
def calculate_years(principal, interest, tax, desired, year=0)
return year if desired<=principal
  calculate_years(principal+(principal*interest-principal*interest*tax),interest,tax,desired,year+=1)
end
