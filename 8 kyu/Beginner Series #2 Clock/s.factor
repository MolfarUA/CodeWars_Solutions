55f9bca8ecaa9eac7100004a


USING: locals math ;
IN: kata

:: past ( h m s -- n )
  h 60 *
  m + 60 *
  s + 1000 *
;
__________________________
USING: calendar kernel ;
IN: kata

: past ( h m s -- n )
    [ 0 0 0 ] 3dip <duration> duration>milliseconds ;
__________________________
USING: arrays kernel math math.polynomials sequences ;
IN: kata

: past ( h m s -- n ) 3array reverse 60 swap polyval 1000 * ;
__________________________
USING: arrays math sequences kernel ;
IN: kata

: past ( h m s -- p ) 3array 0 [ swap 60 * + ] reduce 1000 * ;
__________________________
USING: kernel math ;
IN: kata

: past ( h m s -- n )
    [ 3600 * ] [ 60 * ] [ ] tri*
    + +
    1000 *
    ;
__________________________
USING: kernel math locals ;
IN: kata

:: past ( h m s -- n ) 1000 s 60 m * 3600 h * + + * ;
