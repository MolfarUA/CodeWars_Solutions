5659c6d896bc135c4c00021e
      
      
       identification division.
       program-id. next_smaller_number.
       data division.
       working-storage section.
       01  i                 usage index.
       01  len               usage index.
       01  digits.
            05 dd occurs 0 to 38 times depending on len indexed by j.
              10 ds          pic 9.
       01  t                 pic 9.
      
       linkage section.
       01  n                 pic 9(38).
       01  result            pic S9(38) sign leading.
      
       procedure division using n result.
          move 0 to i result
          inspect n tallying i for leading '0'
          compute len = 38 - i
          move function reverse(n) to digits
          move 1 to j
          search dd varying j
              when j > 1 and ds(j) > ds(j - 1)
                  move j to i
                  move 1 to j
                  search dd varying j
                      when ds(i) > ds(j)
                          move function reverse(digits(i + 1:)) 
                            to result(39 - len:)
                          move ds(j) to result(39 - i:1)
                          move ds(i) to ds(j)
                          move digits(1:i - 1) to result(40 - i:)
                  end-search
          end-search
          if result(39 - len:1) = 0
              move -1 to result
          end-if
          goback.
       end program next_smaller_number.
_______________________________
       identification division.
       program-id. next_smaller_number.
       data division.
       local-storage section.
       01  n-disp            pic z(37)9.
       01  m                 pic 9(37).
       01  r                 pic 9.
       01  d                 pic 9.
       01  s.
           03  l pic 9(2).
           03  chrs.
               05  c pic x occurs 1 to 38 times
                     depending l indexed i j.
       01  t.
           03  len pic 9(2).
           03  xs.
               05  e pic x occurs 1 to 38 times
                     depending len indexed k h.

       linkage section.
       01  n                 pic 9(38).
       01  result            pic S9(38) sign leading.
      
       procedure division using n result.
      
          if n < 10 move -1 to result goback end-if
      
          divide n by 10 giving m remainder r
          perform until m = 0
            compute d = function rem(m, 10)
            if d > r
                exit perform
            else
              divide 10 into m
              move d to r
            end-if
          end-perform
          if m = 0 move -1 to result goback end-if
          compute l i j len = function integer(function log10(n)) + 1
          move n to n-disp
          move function trim(n-disp) to chrs

          perform until c(i - 1) > c(i)
            subtract 1 from i
          end-perform
          perform until c(j) < c(i - 1)
            subtract 1 from j
          end-perform
      
          move c(j) to r
          move c(i - 1) to c(j)
          move r to c(i - 1)
      
          if c(1) = '0' move -1 to result goback end-if
          
          perform varying k from 1 until k = i
            move c(k) to e(k)
          end-perform
          perform test after varying h from l by -1 until h = i
              move c(h) to e(k)
              add 1 to k
          end-perform
          move xs to result
          compute result = result / 10 ** (38 - l)
      
          goback.
       end program next_smaller_number.
_______________________________
       identification division.
       program-id. next_smaller_number.
       data division.
      
       local-storage section.
       01  i                 pic 99.
       01  j                 pic 99.
       01  t                 pic 99.
       01  u                 pic 99.
       01  x                 pic S99 sign leading value -1.
       01  y                 pic S99 sign leading value -1.
       01  ds.
           05 sz             pic 99.
           05 tbl-d          occurs 1 to 38 times 
                             depending on sz.
              10 d           pic 9.
       01  es.
           05 lz             pic 99.
           05 tbl-e          occurs 1 to 38 times 
                             depending on lz.
              10 e           pic 9.
      
       linkage section.
       01  n                 pic 9(38).
       01  r                 pic S9(38) sign leading.
      
       procedure division using n r.
      
          move 1 to sz
          if n > 0 then compute sz = function log10 (n) + 1 end-if
          perform varying i from sz by -1 until i = 0
            compute d(i) = function rem (n, 10)
            divide 10 into n
          end-perform
      
          compute t = sz - 1
          perform varying i from t by -1 until i = 0
            if x > -1 then exit perform end-if
            compute u = i + 1
            perform varying j from u until j > sz
              if d(j) < d(i) then
                move i to x
                exit perform
              end-if
            end-perform
          end-perform
          
          if x = -1 then
            move x to r
            goback
          end-if
      
          compute t = x + 1
          perform varying i from t until i > sz
            if d(i) < d(x) and (y = -1 or d(i) > d(y)) then
              move i to y
            end-if
          end-perform
            
          if d(y) = 0 and x = 1 then
            move -1 to r
            goback
          end-if
      
          move d(x) to t
          move d(y) to d(x)
          move t to d(y)
          compute lz = sz - x
          perform varying i from 1 until i > lz
            move d(i + x) to e(i)
          end-perform
          sort tbl-e on descending e
      
          compute t = x + 1
          move 1 to j
          perform varying i from t until i > sz
            move e(j) to d(i)
            add 1 to j
          end-perform
      
          move 0 to r
          perform varying i from 1 until i > sz
            multiply 10 by r
            add d(i) to r
          end-perform
          
          goback.
       end program next_smaller_number.
