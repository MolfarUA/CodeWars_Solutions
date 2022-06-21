5254ca2719453dcc0b00027d
      
      
       identification division.
       program-id. Permutations recursive.
       data division.
       local-storage section.
       01  ts         pic a(8).
       01  c          pic a.
       01  l          pic 9.
       01  arr.
           03  al     pic 9(5).
           03  a occurs 0 to 50000 times depending al indexed j.
               05  x  pic a(8).
       01 k           index.
       
       linkage section.
       01  s          pic a(8).
       01  result.
           05  ol     pic 9(5).
           05  o      occurs 0 to 50000 times depending ol indexed i.
               07  rs pic a(8).
      
       procedure division using s result.
      
          initialize result
      
          compute l = length function trim(s)
          evaluate l
          when 0   goback
          when 1   move 1 to ol
                   move s to o(1)
                   goback
          end-evaluate
      
          move s(2:) to ts
          call 'Permutations' using ts arr
          move s(1:1) to c
          perform varying j from 1 until j > al
              add 1 to ol
              string c a(j) into o(ol)
              perform varying k from 1 until k > l
              add 1 to ol
              string function trim(a(j)(1:k)) c a(j)(k + 1:) into o(ol)
              end-perform
          end-perform
          
          sort o on ascending rs
          set i to 1
          move o(1) to ts
          perform varying j from 2 until j > ol
          if o(j) <> ts
             add 1 to i
             move o(j) to o(i) ts
          end-if
          end-perform
          move i to ol
      
          goback.
       end program Permutations.
______________________________
       identification division.
       program-id. Permutations recursive.
       data division.
       local-storage section.
       01  k           usage index.
       01  m           pic 9.
       01  w           pic a(8).
       01  c           pic a.
       01  arr.
           05  arr-len pic 9(5).
           05  xs      occurs 0 to 50000 times 
                       depending arr-len 
                       indexed by j.
               08  x   pic a(8).
       linkage section.
       01  s           pic a(8).
       01  result.
           05  res-len pic 9(5).
           05  res     occurs 0 to 50000 times 
                       depending res-len
                       indexed by i.
               08  r   pic a(8).
       procedure division using s result.
      
          initialize result
          perform edge-case
          perform induction
          perform render
          goback.
      
        edge-case.
          move length function trim(s) to m
          if m = 0 then goback end-if
          if m = 1 then
            set res-len to 1
            move s to res(1)
            goback
          end-if
          .
      
        induction.
          move s(2:) to w
          move s(1:1) to c
          call 'Permutations' using by content w by reference arr
          perform varying j from 1 until j > arr-len
            add 1 to res-len
            string c xs(j) into res(res-len)
            perform varying k from 1 until k > m
              add 1 to res-len
              string function trim(xs(j)(1:k)) c xs(j)(k + 1:) 
                into res(res-len)
            end-perform
          end-perform
          .
      
        render.
          sort res on ascending key r
          set i to 1
          move res(1) to w
          perform varying j from 2 until j > res-len
            if res(j) <> w
              add 1 to i
              move res(j) to res(i) w
            end-if
          end-perform
          set res-len to i
          .
          
       end program Permutations.
