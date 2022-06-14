USING: formatting kernel sets ;
IN: kata
: disemvowel ( str -- new-str ) "aeiouAEIOU" without ;
______________________________
USE: sets
IN: kata
: disemvowel ( str -- new-str ) "AEIOUaeiou" without ;
______________________________
USING: sets ;
IN: kata
: disemvowel ( str -- new-str ) "aeiouAEIOU" without ;
______________________________
USING: sequences unicode ;
IN: kata

<PRIVATE
: vowel? ( ch -- ? ) ch>lower "aeiou" member? ;
PRIVATE>

: disemvowel ( str -- str ) [ vowel? ] reject ;
______________________________
USING: regexp ;
IN: kata

: disemvowel ( str -- new-str ) 
  R/ [euioa]/i "" re-replace
;
______________________________
USING: kernel unicode sequences fry ;
IN: kata
: disemvowel ( str -- new-str )  [  {  CHAR: a CHAR: e CHAR: o CHAR: i CHAR: u } swap ch>lower '[ _ = ] any? not ] filter ;
