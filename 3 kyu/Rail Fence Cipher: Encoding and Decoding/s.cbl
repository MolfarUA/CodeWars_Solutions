58c5577d61aefcf3ff000081
      
      
       identification division.
       program-id. Encode.
       data division.
       local-storage section.
       01  gim-arr.
           05 gim-length   pic 9(2).
           05 gim          pic 9(2) occurs 0 to 50 times 
                                    depending on gim-length
                                    indexed by i.
       linkage section.
       01  strng.
           05 s-length     pic 9(2).
           05 s-char       pic x occurs 0 to 50 times 
                                 depending on s-length.
       01  numberRails     pic 9(2).
       01  result.
           05 res-length   pic 9(2).
           05 res          pic x occurs 0 to 50 times 
                                 depending on res-length.
       procedure division using strng numberRails result.
          initialize result 
          call 'Gim' using 
            by content numberRails s-length
            by reference gim-arr
          move gim-length to res-length
          perform varying i from 1 until i > gim-length
            move s-char(gim(i)) to res(i)
          end-perform
          goback.
       end program Encode.
      
       identification division.
       program-id. Decode.
       data division.
       local-storage section.
       01  gim-arr.
           05 gim-length   pic 9(2).
           05 gim          pic 9(2) occurs 0 to 50 times 
                                    depending on gim-length
                                    indexed by i.
       linkage section.
       01  strng.
           05 s-length     pic 9(2).
           05 s-char       pic x occurs 0 to 50 times 
                                 depending on s-length.
       01  numberRails     pic 9(2).
       01  result.
           05 res-length   pic 9(2).
           05 res          pic x occurs 0 to 50 times 
                                 depending on res-length.
       procedure division using strng numberRails result.
          initialize result 
          call 'Gim' using 
            by content numberRails s-length
            by reference gim-arr
          move gim-length to res-length
          perform varying i from 1 until i > gim-length
            move s-char(i) to res(gim(i))
          end-perform
          goback.
       end program Decode.
      
       identification division.
       program-id. Gim.
       data division.
       local-storage section.
       01  rail            pic s9(2) value -1.
       01  phase           pic 9(2) value 0.
       01  x               pic 9(2) value 0.
       01  i               pic 9(2).
       01  lambda.
           05 l0           pic 9(2) value 0.
           05 l1           pic 9(2) value 0.
           05 li           pic 9 value 0.
       linkage section.
       01  n               pic 9(2).
       01  m               pic 9(2).
       01  result.
           05 res-length   pic 9(2).
           05 res          pic 9(2) occurs 0 to 50 times 
                                    depending on res-length.
       procedure division using n m result.
          initialize result
          perform varying i from i until i >= m
            if rail = -1 or x >= m
              add 1 to rail
              set li to 0
              move rail to x phase
              if rail = 0 or rail = n - 1 then
                compute l0 = 2 * (n - 1)
                move l0 to l1
              else
                compute l0 = 2 * (n - rail - 1)
                compute l1 = 2 * rail
              end-if
            end-if
            add 1 to res-length
            compute res(res-length) = x + 1
            if li = 0 then
              add l0 to x
            else
              add l1 to x
            end-if
            compute li = function rem(li + 1, 2)
          end-perform
          goback.
       end program Gim.
_____________________________
       identification division.
       program-id. Encode.
       data division.
       local-storage section.
       01 cnt pic 9(2).
       01 i   usage index.
       01 j   usage index.
       01 k   usage index.
       01 a   pic s9(3).
       01 b   pic s9(3).
       01 it  usage index occurs 2 times.
      
       linkage section.
       01  strng.
           05 l            pic 9(2).
           05 s            pic x occurs 0 to 50 times 
                                  depending on l.
       01  n               pic 9(2).
       01  result.
           05 r            pic 9(2).
           05 res          pic x occurs 0 to 50 times 
                                 depending on r.
      
       procedure division using strng n result.
      
          initialize result
      
          compute cnt = 2 * n - 3
          
          perform varying i from 0 until i = n
            initialize k
            compute a = cnt - 2 * i
            compute b = 2 * i - 1
            move i to j
            compute it(1) = function max(0, a + 1)
            compute it(2) = function max(0, b + 1)
            perform until j >= l
              add 1 to r
              move s(j + 1) to res(r)
              if it(function rem(k, 2) + 1) <> 0
                   add it(function rem(k, 2) + 1) to j
              else add it(function rem(k + 1, 2) + 1) to j end-if
              add 1 to k
            end-perform
          end-perform
      
          goback.
       end program Encode.
      
      
       identification division.
       program-id. Decode.
       data division.
       local-storage section.
       01 cnt pic 9(2).
       01 globalIndex usage index.
       01 i   usage index.
       01 j   usage index.
       01 k   usage index.
       01 a   pic s9(3).
       01 b   pic s9(3).
       01 it  usage index occurs 2 times.
      
       linkage section.
       01  strng.
           05 l            pic 9(2).
           05 s            pic x occurs 0 to 50 times 
                                  depending on l.
       01  n               pic 9(2).
       01  result.
           05 r            pic 9(2).
           05 res          pic x occurs 0 to 50 times 
                                 depending on r.
      
       procedure division using strng n result.
      
          initialize result
      
          compute cnt = 2 * n - 3
          move l to r
          perform varying i from 0 until i = n
            compute a = cnt - 2 * i
            compute b = 2 * i - 1
            compute it(1) = function max(0, a + 1)
            compute it(2) = function max(0, b + 1)
            move i to j
            initialize k
            perform until j >= l
              move s(globalIndex + 1) to res(j + 1)
              if it(function rem(k, 2) + 1) <> 0
                   add it(function rem(k, 2) + 1) to j
              else add it(function rem(k + 1, 2) + 1) to j end-if
              add 1 to k, globalIndex
            end-perform
          end-perform
            
          goback.
       end program Decode.
