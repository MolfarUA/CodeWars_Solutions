module Kata exposing (code, decode)

code : String -> String
code ls =
    case (String.toList ls) of
        ('0'::xs) -> "10" ++ code (String.fromList xs)
        ('1'::xs) -> "11" ++ code (String.fromList xs)
        ('2'::xs) -> "0110" ++ code (String.fromList xs)
        ('3'::xs) -> "0111" ++ code (String.fromList xs)
        ('4'::xs) -> "001100" ++ code (String.fromList xs)
        ('5'::xs) -> "001101" ++ code (String.fromList xs)
        ('6'::xs) -> "001110" ++ code (String.fromList xs)
        ('7'::xs) -> "001111" ++ code (String.fromList xs)
        ('8'::xs) -> "00011000" ++ code (String.fromList xs)
        ('9'::xs) -> "00011001" ++ code (String.fromList xs)
        _ -> ""

decode : String -> String
decode ls =
    case (String.toList ls) of
        ('1'::'0'::xs) ->  "0" ++ (decode (String.fromList xs))
        ('1'::'1'::xs) ->  "1" ++ (decode (String.fromList xs))
        ('0'::'1'::'1'::'0'::xs) ->  "2" ++ (decode (String.fromList xs))
        ('0'::'1'::'1'::'1'::xs) ->  "3" ++ (decode (String.fromList xs))
        ('0'::'0'::'1'::'1'::'0'::'0'::xs) ->  "4" ++ (decode (String.fromList xs))
        ('0'::'0'::'1'::'1'::'0'::'1'::xs) ->  "5" ++ (decode (String.fromList xs))
        ('0'::'0'::'1'::'1'::'1'::'0'::xs) ->  "6" ++ (decode (String.fromList xs))
        ('0'::'0'::'1'::'1'::'1'::'1'::xs) ->  "7" ++ (decode (String.fromList xs))
        ('0'::'0'::'0'::'1'::'1'::'0'::'0'::'0'::xs) ->  "8" ++ (decode (String.fromList xs))
        ('0'::'0'::'0'::'1'::'1'::'0'::'0'::'1'::xs) ->  "9" ++ (decode (String.fromList xs))
        _ -> ""  
