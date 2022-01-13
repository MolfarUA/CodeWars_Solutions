       identification division.
       program-id. IsConstructable.
      
       data division.
       working-storage section.
       01  b           usage index.
       01  c           usage index.
       01  i           usage index.
      
       linkage section.
       01  a           pic 9(10).
       01  result      pic 9.
      
       procedure division using a result.
          compute b = function sqrt(a)
          perform varying i from 1 until i > b
              compute c = function sqrt(a - i * i)
              if c * c + i * i = a
                  move 1 to result
                  goback
              end-if
          end-perform
          move 0 to result.
       end program IsConstructable.
__________________________________
       identification division.
       program-id. IsConstructable.
       data division.
       local-storage section.
       01  i           pic 9(10).
       01  j           pic 9(10).
       01  p           pic 9(10).
       01  x           pic 9(10).
       01  y           pic 9(10)v9(10).
       linkage section.
       01  a           pic 9(10).
       01  r           pic 9.
       procedure division using a r.
          move 1 to r
          compute p = function sqrt(a)
          perform varying i from 1 until i > p
            compute j = a - i * i
            compute x = function sqrt (j)
            compute y = function sqrt (j)
            if x = y then goback end-if
          end-perform
          move 0 to r
          goback.
       end program IsConstructable.
__________________________________
       identification division.
       program-id. IsConstructable.
      
       data division.
       local-storage section.
       01  s           pic 9(10).
       01  p           pic 9(10).
       01  e           pic 9(10).
      
       linkage section.
       01  a           pic 9(10).
       01  result      pic 9.
      
       procedure division using a result.
      
      * Implementation of monadius' Python solution
      * See https://www.codewars.com/kata/reviews/617d4e6a17134c0001526f9c/groups/617d9360ef08800001734b46
          
          move 0 to result
          move 2 to p
      
          compute s = function integer(function sqrt(a))
      
          perform until p > s
            perform varying e from 0 until function rem(a, p) <> 0
              divide p into a
            end-perform
            if function rem(p, 4) =  3
            and function rem(e, 2) = 1
            then goback
            else add 1 to p, end-if
          end-perform
          if function rem(a, 4) <> 3 then move 1 to result, end-if
      
          goback.
       end program IsConstructable.
      
