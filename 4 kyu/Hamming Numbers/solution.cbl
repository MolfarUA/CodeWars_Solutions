       identification division.
       program-id. hamming.
       data division.
       working-storage section.
       01 i2           pic 9(2).
       01 i3           pic 9(2).
       01 i5           pic 9(2).
       01 len          pic 9(8).
       01 tbl.
          05 xs pic 9(16) occurs 1 to 10000 times
                          depending on len.
       linkage section.
      * bounds: 1 <= n <= 5,000
       01  n           pic 9(8). 
       01  result      pic 9(16).
      
       procedure division using n result.
          if len = 0 then
            perform varying i2 from 0 by 1 until i2 > 45
                      after i3 from 0 by 1 until i3 > 28
                      after i5 from 0 by 1 until i5 > 19
              if i2 * 0.6931471805599453 
                    + i3 * 1.0986122886681098
                    + i5 * 1.6094379124341003 < 32 then
                add 1 to len
                compute xs(len) = 2 ** i2 * 3 ** i3 * 5 ** i5
              end-if
            end-perform
            sort xs on ascending key xs
          end-if
          compute result = xs(n).
       end program hamming.
      
___________________________________________________
       identification division.
       program-id. hamming.
       data division.
       working-storage section.
       01 x            pic 9(16).
       01 y            pic 9(16).
       01 z            pic 9(16).
       01 len          pic 9(8).
       01 tbl based.
          05 xs pic 9(16) occurs 1 to 9999 times 
                          depending on len
                          indexed by i, i2, i3, i4.
       linkage section.
       01  n           pic 9(8). 
       01  result      pic 9(16).
       procedure division using n result.
          if len = 0
            compute len = 5000
            allocate tbl
            compute xs(1) result i2 i3 i4 = 1
            move 2 to x
            move 3 to y
            move 5 to z
            perform varying i from 2 by 1 until i > len
              compute xs(i) = function min (x, function min (y, z))
              if xs(i) = x then
                set i2 up by 1
                compute x = 2 * xs(i2)
              end-if
              if xs(i) = y then
                set i3 up by 1
                compute y = 3 * xs(i3)
              end-if
              if xs(i) = z then
                set i4 up by 1
                compute z = 5 * xs(i4)
              end-if
            end-perform
          end-if
          move xs(n) to result
          goback.
       end program hamming.
