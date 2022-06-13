module Welcome where
import Text.Printf

sayhello :: [String] -> String -> String -> String
sayhello n c s = printf "Hello, %s! Welcome to %s, %s!" (unwords n) c s
_______________________________________
module Welcome where
sayhello :: [String] -> String -> String -> String
sayhello names city state = "Hello, " ++ unwords names ++ "! Welcome to " ++ city ++ ", " ++ state ++ "!"
_______________________________________
module Welcome where
import Text.Printf

sayhello :: [String] -> String -> String -> String
sayhello = printf "Hello, %s! Welcome to %s, %s!" . unwords
_______________________________________
module Welcome where
sayhello :: [String] -> String -> String -> String
sayhello a b c = "Hello, " ++ unwords a ++ "! Welcome to " ++ b ++ ", " ++ c ++ "!"
_______________________________________
module Welcome where
sayhello :: [String] -> String -> String -> String
sayhello n s p = "Hello, " ++ unwords n ++ "! Welcome to " ++ s ++ ", " ++ p ++"!"
