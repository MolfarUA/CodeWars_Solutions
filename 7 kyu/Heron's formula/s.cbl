57aa218e72292d98d500240f
      
      
       identification division.
       program-id. heron.
       AUTHOR. "ejini战神".
       data division.   
       WORKING-STORAGE SECTION.
       01 s                  pic 9(4)V9(2).
       linkage section.
       01  x                 pic 9(3).
       01  y                 pic 9(3).
       01  z                 pic 9(3).
       01  result            pic 9(8)v9(2).      
       procedure division using x y z result.
           COMPUTE s = (x + y + z) / 2
           COMPUTE result ROUNDED = FUNCTION SQRT( s * (s - x) * (s - y) 
                                     * (s - z)).
       end program heron.
________________________
       identification division.
       program-id. heron.
       data division.
      
       local-storage section.
       01  s                 pic 9(10)v9(4).
      
       linkage section.
       01  x                 pic 9(3).
       01  y                 pic 9(3).
       01  z                 pic 9(3).
       01  result            pic 9(8)v9(2).
      
       procedure division using x y z result.
           compute s = (x + y + z) / 2
           compute s = function sqrt(s * (s - x) * (s - y) * (s - z))
           compute result rounded = s
           goback.
       end program heron.
________________________
       identification division.
       program-id. heron.
       data division.
       working-storage section.
       01  p                 pic 9(4)v9(1).
      
       linkage section.
       01  x                 pic 9(3).
       01  y                 pic 9(3).
       01  z                 pic 9(3).
       01  result            pic 9(8)v9(2).
      
       procedure division using x y z result.
           compute p = (x + y + z) / 2
           compute result rounded = 
                function sqrt(p * (p - x) * (p - y) * (p - z)).
       end program heron.
