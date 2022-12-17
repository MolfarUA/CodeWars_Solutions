55df87b23ed27f40b90001e5
      
      
       identification division.
       program-id. CalculateSpecial.
       data division.
       local-storage section.
       01  alpha           pic x(16) value '0123456789abcdef'.
       01  d               pic 9(3).
       01  r               pic 9(3) value 0.
       01  m               pic 9(3).
       linkage section.
       01  i               pic 9(2).
       01  t               pic 9(2).
       01  result.
           05 res-len      pic 9(3).
           05 res.          
              07 xs        pic x occurs 0 to 200 times 
                                 depending on res-len.
       procedure division using t i result.
          initialize result
          add 1 to res-len
          move alpha(t + 1: 1) to xs(res-len)
          move t to d
          perform forever
            compute m = t * d + r
            divide i into m giving r remainder d
            add 1 to res-len
            move alpha(d + 1: 1) to xs(res-len)
            if d = 1 and r = 0 then
              exit perform
            end-if
          end-perform
          move function reverse(res) to res
          goback.
       end program CalculateSpecial.
____________________________
       identification division.
       program-id. CalculateSpecial.
       data division.
       local-storage section.
       01 alpha pic x(16) value '0123456789abcdef'.
       01 digit    pic 9(2).
       01 dividend pic 9(4).
       01 divisor  pic 9(3).
   
      
       linkage section.
       01  lastDigit       pic 9(2).
       01  base            pic 9(2).
       01  result.
           05 resLength    pic 9(3).
           05 res          pic x occurs 0 to 200 times 
                                 depending on reslength.
      
       procedure division using lastDigit base result.
      
          initialize result

          move lastDigit to dividend
          compute divisor = lastDigit * base - 1
          perform until digit = lastDigit and dividend = lastDigit
            multiply base by dividend
            divide dividend by divisor giving digit remainder dividend
            add 1 to resLength
            move alpha(digit + 1: 1) to res(resLength)
          end-perform
      
          goback.
       end program CalculateSpecial.
