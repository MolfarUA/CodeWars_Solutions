52f677797c461daaf7000740
      
      
       identification division.
       program-id. solution.
      
       data division.
       local-storage section.
       01 x                pic 9(20).
       01 y                pic 9(20).
      
       linkage section.
       01  a.
           05 arr-length   pic 9(5).
           05 xs           pic 9(20) occurs 0 to 50000 times 
                                  depending on arr-length
                                  indexed by i.
       01  result      pic 9(20).
      
       procedure division using a result.
      
          compute result = xs(1)
      
          perform varying i from 2 until i > arr-length
                move xs(i) to x
                perform until x = 0
                    move x to y
                    compute x = function rem(result, x)
                    move y to result
                end-perform
          end-perform
      
          multiply arr-length by result
      
          goback.
       end program solution.
_______________________________
       identification division.
       program-id. solution.
       data division.
       local-storage section.
       01  x          pic 9(20).
       01  y          pic 9(20).
       linkage section.
       01  a.
           05 n       pic 9(5).
           05 xs      pic 9(20) occurs 0 to 50000 times 
                                depending on n
                                indexed by i.
       01  r          pic 9(20).
       procedure division using a r.
          move 0 to r
          if n = 0 then goback end-if
          move xs(1) to r
          perform varying i from 2 until i > n
            move xs(i) to x
            call 'gcd' using by content r x by reference y
            move y to r
          end-perform
          multiply n by r giving r
          goback.
       end program solution.
      
       identification division.
       program-id. gcd.
       data division.
       local-storage section.
       01 c           pic 9(20).
       01 a           pic 9(20).
       linkage section.
       01 x           pic 9(20).
       01 b           pic 9(20).
       01 r           pic 9(20).
       procedure division using x b r.
           move x to a
           perform until b = 0,
              move b to c,
              compute b = function rem(a, b),
              move c to a,
           end-perform
           move a to r
           goback.
       end program gcd.
_______________________________
       identification division.
       program-id. solution.
      
       data division.
       working-storage section.
       01  a               pic 9(20).
       01  b               pic 9(20).
      
       linkage section.
       01  arr.
           05 arr-length   pic 9(5).
           05 xs           pic 9(20) occurs 0 to 50000 times 
                                  depending on arr-length
                                  indexed by i.
       01  result          pic 9(20).
      
       procedure division using arr result.
          compute result = xs(1)
          perform varying i from 2 until i > arr-length
              compute a = result
              compute b = xs(i)
              perform until b = 0
                  compute result = b
                  compute b = function mod(a, b)
                  compute a = result
              end-perform
          end-perform
          multiply arr-length by result
          goback.
       end program solution.
