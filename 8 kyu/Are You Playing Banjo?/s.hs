53af2b8861023f1d88000832


module Banjo where

areYouPlayingBanjo :: String -> String
areYouPlayingBanjo name@(c:_) 
  | c `elem` "rR" = name ++ " plays banjo"
  | otherwise = name ++ " does not play banjo"
________________________________
module Banjo where

areYouPlayingBanjo :: String -> String
areYouPlayingBanjo name@(c:_) | c `elem` "rR" = name ++ " plays banjo"
areYouPlayingBanjo name                       = name ++ " does not play banjo"
________________________________
module Banjo where

areYouPlayingBanjo :: String -> String
areYouPlayingBanjo name = name ++ " " ++ playStr name ++ " banjo"
  where
    playStr ('r':_) = "plays"
    playStr ('R':_) = "plays"
    playStr _ = "does not play"
