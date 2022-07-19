51c8e37cee245da6b40000bd


USING: kernel splitting sequences sequences.extras unicode ;
IN: strip-comments

: strip-comments ( text markers -- result ) 
  [ "\n" split ] dip
  [ [ index not ] curry take-while [ blank? ] trim-tail ] curry 
  map "\n" join ;
__________________________________
USING: splitting kernel fry sets sequences sequences.extras ;
IN: strip-comments

: strip-comments ( text markers -- result )
    [ "\n" split ] dip
    '[ [ _ in? not ] take-while [ CHAR: space = ] trim ] map
    "\n" join ;
__________________________________
USING: kernel splitting sequences ;
IN: strip-comments

: strip-line ( line markers -- line )
  [ member? ] curry dupd find drop
  [ head [ 32 = ] trim-tail ] when* ;

: map-lines ( str quot -- str ) [ "\n" split ] dip map "\n" join ; inline

: strip-comments ( text markers -- result ) [ strip-line ] curry map-lines ;
