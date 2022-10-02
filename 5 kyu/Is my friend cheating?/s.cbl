5547cc7dcad755e480000004
      
      
       identification division.
       program-id. RemoveNb.
       data division.
       local-storage section.
       01  m                 pic 9(16).
       01  x                 pic 9(8).
       01  y                 pic 9(8).
       linkage section.
       01  n                 pic 9(8).
       01  r.
           05 i              pic 9(2).
           05 res            occurs 0 to 20 times
                             depending on i.
              07 a           pic 9(8).
              07 b           pic 9(8).
       procedure division using n r.
          move 0 to i
          compute m = (n * (n + 1)) / 2
          perform varying x from 1 until x > n
            compute y = (m - x) / (x + 1)
            if y <= n and x * y = m - x - y then
              add 1 to i
              move x to a(i)
              move y to b(i)
            end-if
          end-perform
          goback.
       end program RemoveNb.
______________________________
       identification division.
       program-id. RemoveNb.
       data division.
       working-storage section.
       01  s                 pic 9(16).
       01  x                 pic 9(10).
      
       linkage section.
       01  n                 pic 9(8).
       01  result.
           05 res-length     pic 9(2).
           05 res            occurs 0 to 20 times
                             depending on res-length.
              07 a           pic 9(8).
              07 b           pic 9(8).
      
       procedure division using n result.
          compute s = n * (n + 1) / 2
          compute x = (s - n) / (n + 1)
          perform varying x from x until x > n
              if function mod(s - x, x + 1) = 0
                  add 1 to res-length
                  compute a(res-length) = x
                  compute b(res-length) = (s - x) / (x + 1)
              end-if
          end-perform.
       end program RemoveNb.
______________________________
       identification division.
       program-id. RemoveNb.
       data division.
       local-storage section.
       01  s                 pic 9(16).
       01  i                 pic 9(8).
      
       linkage section.
       01  n                 pic 9(8).
       01  result.
           05 k              pic 9(2).
           05 res            occurs 0 to 20 times
                             depending k.
              07 a           pic 9(8).
              07 b           pic 9(8).
      
       procedure division using n result.

          compute s = n * (n + 1) / 2
      
          move 0 to k
          
          perform varying i
                  from function integer((s - n) / (n + 1))
                       until i > n
           if function rem(s - i, i + 1) = 0
              add 1 to k, move i to a of res(k)
              move function integer((s - i) / (i + 1)) to b of res(k)
          end-perform
      
          goback.
       end program RemoveNb.
