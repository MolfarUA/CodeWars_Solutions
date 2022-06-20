55466989aeecab5aac00003e


USING: kernel math math.order sequences ;
IN: rect2square

: chop ( m n -- m' n' )
    [ min ] [ - abs ] 2bi ;

: squareify ( l w -- seq )
    [ dup zero? not ] [ chop over ] produce 2nip ;

: sq-in-rect ( l w -- seq )
    2dup = [ 2drop f ] [ squareify ] if ;
______________________________
USING: kernel sequences vectors math math.order prettyprint ;
IN: rect2square

: sq-in-rect-help ( l w -- seq )
  2dup = [ drop 1vector ]
  [ [ min ] [ max ] 2bi dupd over - sq-in-rect-help [ push ] keep ] if
  ;

: sq-in-rect ( l w -- seq )
  2dup = [ 2drop f ]
  [ [ min ] [ max ] 2bi dupd over - sq-in-rect-help [ push ] keep reverse ] if
  ;
______________________________
USING: kernel math math.order sequences ;
IN: rect2square

: sq-in-rect ( l w -- seq )
  2dup = [ 2drop f ] [
    [ over 0 > ] [ [ max ] [ min ] 2bi [ - ] keep dup ] produce 2nip
  ] if ;
