USING: math ;
IN: kata
: digital-root ( n -- root ) 1 - 9 mod 1 + ;

________________________________
USING: math kernel ;
IN: kata
: digital-root ( n -- root ) dup 0 = [ ] [ 9 mod dup 0 = swap 9 swap ? ] if ;

________________________________
USING: math kernel ;
IN: kata
: digital-root ( n -- root ) dup 0 = [ ] [ 9 mod dup 0 = swap 9 swap ? ] if ;

________________________________
USING: kernel math sequences ;
IN: kata

: digits ( n -- seq )
  [ dup 0 > ] [ 10 /mod ] produce nip ;

: digital-root ( n -- root )
  digits 0 [ + ] reduce dup 9 > [ digital-root ] when ;
  
________________________________
USING: kernel locals math math.parser sequences ;
IN: kata

: digital-root ( n -- root ) dup 9 > [
    number>string [ CHAR: 0 - ] map sum digital-root
  ] when ; recursive
