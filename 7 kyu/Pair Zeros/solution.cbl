       identification division.
       program-id. PairZeros.
       data division.
       local-storage section.
       01  z                 pic 9(2).
      
       linkage section.
       01  arr.
           05 arr-length     pic 9(2).
           05 xs             pic 9(2) occurs 0 to 50 times 
                                      depending on arr-length
                                      indexed by i.
       01  result.
           05 res-length     pic 9(2).
           05 res            pic 9(2) occurs 0 to 50 times 
                                     depending on res-length.
      
       procedure division using arr result.
      
          move 0 to z, res-length
          perform varying i from 1 until i > arr-length
              if xs(i) = 0
                  add 1 to z
                  if function rem(z, 2) = 1
                     add 1 to res-length
                     move 0 to res(res-length)
                  end-if
              else
                  add 1 to res-length
                  move xs(i) to res(res-length)
              end-if
           end-perform
      
          goback.
       end program PairZeros.
      
_____________________________________
       identification division.
       program-id. PairZeros.
       data division.
       local-storage section.
       01  m                 pic 9(2).
       linkage section.
       01  arr.
           05 arr-length     pic 9(2).
           05 xs             pic 9(2) occurs 0 to 50 times 
                                      depending on arr-length
                                      indexed by i.
       01  result.
           05 res-length     pic 9(2).
           05 res            pic 9(2) occurs 0 to 50 times 
                                      depending on res-length.
       procedure division using arr result.
          move 0 to m, res-length
          perform varying i from 1 until i > arr-length
              if xs(i) = 0
                  add 1 to m
                  if function mod(m, 2) = 1
                     add 1 to res-length
                     move 0 to res(res-length)
                  end-if
              else
                  add 1 to res-length
                  move xs(i) to res(res-length)
              end-if
          end-perform
          goback.
       end program PairZeros.
