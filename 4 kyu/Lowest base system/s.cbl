58bc16e271b1e4c5d3000151
      
      
       identification division.
       program-id. GetMinBase.
      
       data division.
       working-storage section.
       01 k           usage index.
       01 b           pic 9(10).

       linkage section.
       01 n           pic 9(20).
       01 result      pic 9(20).
      
       procedure division using n result.
          compute k = function abs(function log(n) / function log(2))
          perform varying k from k by -1 until k < 2
              compute b = function abs(n ** (1 / k) + 1)
              perform varying b from b by -1 until b < 2
                  evaluate (b ** (k + 1) - 1) / (b - 1)
                      when n   move b to result; goback
                      when < n exit perform
                  end-evaluate
              end-perform
          end-perform
          compute result = n - 1
          goback.
       end program GetMinBase.
______________________________________
       identification division.
       program-id. GetMinBase.
       data division.
       local-storage section.
       01 n           pic 9(20).
       01 b           pic 9(20).
       01 z           pic 9(20).
       linkage section.
       01 x           pic 9(20).
       01 r           pic 9(20).
       procedure division using x r.
      
          subtract 1 from x giving r
          compute n rounded mode toward-greater
            = function log(x) / function log(2)
          perform until n = 0
            compute b = x ** function abs(1.0 / n)
            perform verify
            subtract 1 from b
            perform verify
            subtract 1 from n
          end-perform
          goback.
      
          verify.
            move x to z
            perform until function rem(z, b) <> 1
              compute z = (z - 1) / b
            end-perform
            if z = 0 then move b to r, goback end-if
            .      
          
       end program GetMinBase.
______________________________________
       identification division.
       program-id. GetMinBase.
      
       data division.
       local-storage section.
       01 k    pic 9(20).
       01 b    pic 9(20).
       01 i    pic 9(20).
       01 t    pic 9(32).
       01 s    pic 9(32).
      
       linkage section.
       01 n           pic 9(20).
       01 result      pic 9(20).
      
       procedure division using n result.
      
      * Implementation of monadius' JavaScript solution
      * https://www.codewars.com/kata/reviews/58bc1f5602f48e8f7000009a/groups/5aebaa7d116e09861200086b
      
          initialize result
          compute k rounded mode toward-greater = 
                    function log(n) / function log(2)
          add 1 to k
      
          perform until k = 1
            compute b rounded mode toward-greater =
                      n ** function abs(1.0 / k)
            add 1 to b
            perform until b = 1
              move 0 to s
              move 1 to t
              perform varying i from 0 until i > k
                add t to s
                multiply b by t
              end-perform
              evaluate s
              when n
                  move b to result
                  goback
              when < n
                  exit perform
              end-evaluate
              subtract 1 from b
            end-perform
            subtract 1 from k
          end-perform
      
          compute result = n - 1
      
          goback.
       end program GetMinBase.
