5b609ebc8f47bd595e000627


solution = (arr_val, arr_unit) ->
  massUnits = 
    kg: 1
    g: 1.0e-3
    mg: 1.0e-6
    μg: 1.0e-9
    lb: 0.453592
  distanceUnits = 
    m: 1
    cm: 1.0e-2
    mm: 1.0e-3
    μm: 1.0e-6
    ft: 0.3048
  massObjA = arr_val[0] * massUnits[arr_unit[0]]
  massObjB = arr_val[1] * massUnits[arr_unit[1]]
  distance = arr_val[2] * distanceUnits[arr_unit[2]]
  6.67e-11 * massObjA * massObjB / (distance * distance)
____________________________________
solution = (arrVal, arrUnit) ->
  convert = 
    kg: 1
    g: 1e-3
    mg: 1e-6
    μg: 1e-9
    lb: 0.453592
    m: 1
    cm: 1e-2
    mm: 1e-3
    μm: 1e-6
    ft: 0.3048
  mass1 = arrVal[0] * convert[arrUnit[0]]
  mass2 = arrVal[1] * convert[arrUnit[1]]
  dist  = arrVal[2] * convert[arrUnit[2]]
  6.67e-11 * mass1 * mass2 / (dist * dist)
____________________________________
solution = (arr, units) ->
  converter = { m: 1, cm: 0.01, mm: 1e-3, μm: 1e-6, ft: 0.3048, kg: 1, g: 1e-3, mg: 1e-6, μg: 1e-9, lb: 0.453592 }
  G = 6.67e-11
  [m1, m2, r] = arr.map (v, i) -> v * converter[units[i]]
  G * m1 * m2/ (r ** 2)
