563f037412e5ada593000114


calculateYears = (principal, interest, tax, desired) ->
  effectiveInterest = interest * (1 - tax)
  # principal * (1 + effectiveInterest) ** n = desired
  n = Math.log(desired / principal) / Math.log(1 + effectiveInterest)
  Math.ceil n
_________________________
calculateYears = (principal, interest, tax, desired) ->
  year = 0
  while principal < desired
    principal += principal * interest * (1 - tax)
    year++
  year
_________________________
calculateYears = (principal, interest, tax, desired) ->
    Math.ceil Math.log(desired / principal) / Math.log(interest * (1 - tax) + 1)
_________________________
calculateYears = (principal, interest, tax, desired) ->
  growth = interest * (1-tax)
  Math.ceil Math.log(desired/principal) / Math.log(1+growth)
