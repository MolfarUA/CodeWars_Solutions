55466989aeecab5aac00003e
      
      
       identification division.
       program-id. SqInRect.
       data division.
      
       linkage section.
       01  lng              pic 9(4).
       01  wdth             pic 9(4).
       01  result.
           05  resLength    pic 9(4).
           05  res pic 9(3) occurs 0 to 1000 times 
                            depending on resLength.
      
       procedure division using lng wdth result.
          move 0 to resLength
          if lng = wdth then goback end-if
          perform until lng = 0
              add 1 to resLength
              move function min(lng, wdth) to res(resLength)
              if lng < wdth
                  subtract lng from wdth
              else
                  subtract wdth from lng
              end-if
          end-perform.
       end program SqInRect.
______________________________
       identification division.
       program-id. SqInRect.
       data division.
       local-storage section.
       01  t                pic 9(4).
       linkage section.
       01  a                pic 9(4).
       01  b                pic 9(4).
       01  result.
           05  sz           pic 9(4).
           05  arr          pic 9(3) 
                            occurs 0 to 1000 times 
                            depending on sz.
       procedure division using a b result.
          initialize result
          if a = b then exit paragraph end-if
          perform forever
            if a = b then exit perform end-if
            if a < b then
              move a to t
              move b to a
              move t to b
            end-if
            add 1 to sz
            move b to arr(sz)
            subtract b from a
          end-perform
          add 1 to sz
          move b to arr(sz)
          goback.
       end program SqInRect.
______________________________
       identification division.
       program-id. SqInRect.
       data division.
       local-storage section.
       01  l                pic 9(4).
       01  w                pic 9(4).
       01  tmp              pic 9(3).
      
       linkage section.
       01  lng              pic 9(4).
       01  wdth             pic 9(4).
       01  result.
           05  resLength    pic 9(4).
           05  res pic 9(3) occurs 0 to 1000 times 
                            depending on resLength.
      
       procedure division using lng wdth result.
      
          initialize result
      
          evaluate true
          when lng = wdth 
              goback
          when lng < wdth
              move wdth to l
              move lng  to w
          when other
              move lng  to l
              move wdth to w
          end-evaluate
      
          perform varying resLength from 1 until l = w
              move w to res(resLength)
              subtract w from l
              if l < w
                  move l to tmp
                  move w to l
                  move tmp to w
              end-if
          end-perform
          
          move w to res(resLength)
      
          goback.
       end program SqInRect.
