53573877d5493b4d6e00050c


capital = (capitals) ->
  capitals.map((x) -> "The capital of #{x.state || x.country} is #{x.capital}")
_________________________
capital = (capitals) ->
    "The capital of #{entry.state or entry.country} is #{entry.capital}" for entry in capitals
_________________________
capital = (capitals) ->
  capitals.map (c) -> "The capital of #{c.state || c.country} is #{c.capital}"
