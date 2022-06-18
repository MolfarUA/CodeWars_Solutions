55fab1ffda3e2e44f00000c6


module Codewars.Cockroach where

cockroachSpeed :: Double -> Integer
cockroachSpeed s = floor (s * 1000 / 36)
__________________________
module Codewars.Cockroach where

cockroachSpeed :: Double -> Integer
cockroachSpeed = floor . (/3600) . (*100000)
__________________________
module Codewars.Cockroach where

cockroachSpeed :: Double -> Integer
cockroachSpeed s = floor $ s * cm_per_km / seconds_per_hour
  where
  cm_per_km = 100000
  seconds_per_hour = 3600
__________________________
module Codewars.Cockroach where

cockroachSpeed :: Double -> Integer
cockroachSpeed s = floor $ 1000 / 36 * s
__________________________
module Codewars.Cockroach where

cockroachSpeed :: Double -> Integer
cockroachSpeed kmh = floor cms
  where cmh = kmh * (1000 * 100)
        cms = cmh / (60 * 60)
__________________________
module Codewars.Cockroach where

cockroachSpeed :: Double -> Integer
cockroachSpeed s = let sc = 1000.0 / 36.0 in floor (sc * s )
