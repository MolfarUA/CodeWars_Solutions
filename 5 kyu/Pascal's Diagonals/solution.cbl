       identification division.
       program-id. generateDiagonal.
       data division.
       linkage section.
       01  n                 pic 9(3).
       01  l                 pic 99.
       01  result.
           05 res-length     pic 99.
           05 res            pic 9(20) occurs 0 to 20 times 
                                  depending on res-length
                                  indexed by i, j.
       procedure division using n l result.
          move function max (l, 0) to res-length
          perform varying i from 1 until i > l
            move 1 to res(i)
          end-perform
          perform varying i from 1 until i > n
            perform varying j from 2 until j > l
              compute res(j) = res(j) + res(j - 1)
            end-perform
          end-perform
          goback.
       end program generateDiagonal.
_______________________________
       identification division.
       program-id. generateDiagonal.
       data division.

       linkage section.
       01  n                 pic 9(3).
       01  l                 pic 99.
       01  result.
           05 res-length     pic 99.
           05 res            pic 9(20) occurs 0 to 20 times 
                                  depending on res-length indexed by i.
      
       procedure division using n l result.
          move l to res-length
          if l = 0 then goback end-if
          move 1 to res(1)
          perform varying i from 1 until i = l
              compute res(i + 1) = res(i) * (n + i) / i
          end-perform.
       end program generateDiagonal.
_______________________________
       identification division.
       program-id. generateDiagonal.
       data division.
       local-storage section.
       01  i                 pic 9(3).
       01  j                 pic 99.
       linkage section.
       01  n                 pic 9(3).
       01  l                 pic 99.
       01  result.
           05 res-length     pic 99.
           05 res            pic 9(20) occurs 0 to 20 times 
                                  depending on res-length.
      
       procedure division using n l result.
      
          move l to res-length
          perform varying i from 1 until i > l
            move 1 to res(i)
          end-perform
          perform varying i from 1 until i > n
            perform varying j from 2 until j > l
              compute res(j) = res(j) + res(j - 1)
            end-perform
          end-perform
      
          goback.
       end program generateDiagonal.
_______________________________
