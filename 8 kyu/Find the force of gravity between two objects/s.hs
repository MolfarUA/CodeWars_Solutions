5b609ebc8f47bd595e000627


module Gravity (solution) where

g = 6.67 * 1e-11

toMeters :: (Double, String) -> Double
toMeters (v, u)
    | u == "μm" = v * 1e-6
    | u == "mm" = v * 1e-3
    | u == "cm" = v * 1e-2
    | u == "ft" = v * 0.3048
    | otherwise = v

toKilograms :: (Double, String) -> Double
toKilograms (v, u)
    | u == "μg" = v * 1e-9
    | u == "mg" = v * 1e-6
    | u == "g" = v * 1e-3
    | u == "lb" = v * 0.453592
    | otherwise = v

solution :: [Double] -> [String] -> Double
solution values units = 
    let d = zip values units
        obj1 = toKilograms (d !! 0)
        obj2 = toKilograms (d !! 1)
        dist = toMeters (d !! 2)
    in g*obj1*obj2/(dist^2)
____________________________________
module Gravity (solution) where

g = 6.67 * 10 ** (-11)

toMass :: String -> Double -> Double
toMass "kg" = id
toMass "g" = (* 10 ** (-3))
toMass "mg" = (* 10 ** (-6))
toMass "μg" = (* 10 ** (-9))
toMass "lb" = (* 0.453592) . toMass "kg"

toDistance :: String -> Double -> Double
toDistance "m" = id
toDistance "cm" = (* 10 ** (-2))
toDistance "mm" = (* 10 ** (-3))
toDistance "μm" = (* 10 ** (-6))
toDistance "ft" = (* 0.3048) . toDistance "m"

solution :: [Double] -> [String] -> Double
solution ([m1, m2, d]) ([u1, u2, ud]) =
 g * (toMass u1 m1) * (toMass u2 m2) / (toDistance ud d ** 2)
