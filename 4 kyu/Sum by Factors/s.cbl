54d496788776e49e6b00052f
      
      
       identification division.
       program-id. SumOfDivided.
       data division.
       working-storage section.
       01  n       usage index.
       01  d       usage index.
      
       linkage section.
       01  arr.
           05 arr-length     pic 9(2).
           05 xs             pic s9(6) occurs 0 to 20 times 
                                  depending on arr-length indexed i j.
       01  result.
           05 res-length     pic 9(3).
           05 pair           occurs 0 to 300 times
                             depending on res-length.
              07 factor      pic 9(6).
              07 sumByFactor pic s9(8). 
      
       procedure division using arr result.
          move 0 to res-length
          perform varying i from 1 until i > arr-length
              move function abs(xs(i)) to n
              move 2 to d
              perform until d * d > n
                  if function mod(n, d) = 0
                      perform test after until function mod(n, d) <> 0
                          divide d into n
                      end-perform
                      add 1 to res-length
                      move d to factor(res-length)
                      move xs(i) to sumByFactor(res-length)
                  end-if
                  add 1 to d
              end-perform
              if n > 1
                  add 1 to res-length
                  move n to factor(res-length)
                  move xs(i) to sumByFactor(res-length)
              end-if
          end-perform
      
          sort pair on ascending key factor
          move 1 to j
          perform varying i from 2 until i > res-length
              if factor(j) = factor(i)
                  add sumByFactor(i) to sumByFactor(j)
              else
                  add 1 to j
                  if j < i move pair(i) to pair(j) end-if
              end-if
          end-perform
          move function min(j, res-length) to res-length      
          goback.
       end program SumOfDivided.
________________________________________________
       identification division.
       program-id. SumOfDivided.
       data division.
       local-storage section.
      * prime factors section
       01  p-m               pic 9(6).
       01  p-f               pic 9(6).
       01  p-arr.
           05 p-len          pic 9(3).
           05 p-xs           pic 9(6) occurs 0 to 999 times 
                                      depending on p-len
                                      indexed by p-i.
      * many prime factors section
       01  mp-arr.
           05 mp-len         pic 9(4).
           05 mp-xs                   occurs 0 to 9999 times 
                                      depending on mp-len
                                      indexed by mp-i.
              08 mp-e        pic 9(6).
       01  mp-set.
           05 mps-len        pic 9(3).
           05 mps-xs         pic 9(6) occurs 0 to 999 times 
                                      depending on mps-len
                                      indexed by mps-i.
      * sum of divided section
       01  m                 pic s9(8).
       01  e                 pic s9(6).
       01  p                 pic 9(6).
       linkage section.
       01  lst-arr.
           05 lst-len        pic 9(2).
           05 lst-xs         pic s9(6) occurs 0 to 20 times 
                                       depending on lst-len
                                       indexed by lst-i.
       01  result.
           05 res-length     pic 9(3).
           05 pair           occurs 0 to 300 times
                             depending on res-length.
              07 factor      pic 9(6).
              07 sumByFactor pic s9(8). 
       procedure division using lst-arr result.
      
          initialize result
          perform many-prime-factors
          perform varying mps-i from 1 until mps-i > mps-len
            set m to 0
            move mps-xs(mps-i) to p
            perform varying lst-i from 1 until lst-i > lst-len
              compute e = lst-xs(lst-i)
              if function rem (function abs (e), p) = 0 then
                add e to m
              end-if
            end-perform
            add 1 to res-length
            move p to factor(res-length)
            move m to sumByFactor(res-length)
          end-perform
          goback.
      
          many-prime-factors.
            initialize mp-arr mp-set
            perform varying lst-i from 1 until lst-i > lst-len
              compute p-m = function abs (lst-xs(lst-i))
              perform prime-factors
              perform varying p-i from 1 until p-i > p-len
                add 1 to mp-len
                move p-xs(p-i) to mp-xs(mp-len)
              end-perform
            end-perform
            sort mp-xs on ascending key mp-e
            set mps-len to 1
            move mp-xs(1) to mps-xs(1)
            perform varying mp-i from 2 until mp-i > mp-len
              if mp-xs(mp-i) <> mp-xs(mp-i - 1) then
                add 1 to mps-len
                move mp-xs(mp-i) to mps-xs(mps-len)
              end-if
            end-perform
            .
      
          prime-factors.
            initialize p-arr
            set p-f to 2
            perform until p-f * p-f > p-m
              if function rem (p-m, p-f) = 0 then
                add 1 to p-len
                move p-f to p-xs(p-len)
                perform until function rem (p-m, p-f) <> 0
                  divide p-f into p-m
                end-perform
              end-if
              add 1 to p-f
            end-perform
            if p-m > 1 then
              add 1 to p-len
              move p-m to p-xs(p-len)
            end-if
            .
      
       end program SumOfDivided.
________________________________________________
       identification division.
       program-id. SumOfDivided.
       data division.
       local-storage section.
      * store prime numbers that remain after `naive` factorization
       01 extra occurs 20 times indexed k.
          05 n pic 9(6).
      * store the absolute values of numbers in arr, they will be used to perform the prime factorization
       01 clone.
          03 cln pic 9(6) occurs 0 to 20 times depending on l.
      * the values in `cycle`  allow to generate factors >= 11, avoiding multiples of 2, 3, 5, and 7
       01 cycle.
          03  pic 9  value 2.
          03  pic 9  value 4.
          03  pic 9  value 2.
          03  pic 9  value 4.
          03  pic 9  value 6.
          03  pic 9  value 2.
          03  pic 9  value 6.
          03  pic 9  value 4.
       01 redefines cycle.
          03 c pic 9 occurs 8 times indexed h.
      * first prime numbers, that will be handled separately first
       01 f.
          03  pic 9 value 2.
          03  pic 9 value 3.
          03  pic 9 value 5.
          03  pic 9 value 7.
       01 redefines f.
          03 firstPrimes pic 9 occurs 4 times.
       01  flag pic 9.
       01  p    pic 9(6).
       01  i usage index.
       01  j usage index.
      
       linkage section.
       01  arr.
           05 l              pic 9(2).
           05 xs             pic s9(6)
                             occurs 0 to 20 times depending on l.
       01  result.
           05 r              pic 9(3).
           05 res            occurs 0 to 300 times depending on r.
              07 primes      pic 9(6).
              07 sums        pic s9(8). 
      
       procedure division using arr result.
      
          initialize result
          perform varying i from 1 until i > l
            move xs(i) to cln(i)
          end-perform
      
      * factors 2, 3, 5 and 7
          perform varying i from 1 until i = 5
            move firstPrimes(i) to p
      * flag checks p is a factor of some number
            move 0 to flag
            perform varying j from 1 until j > l
              if function rem(cln(j), p) = 0
                 move 1 to flag
                 perform reduce
              end-if
            end-perform
      * a new prime factor was found, add it to result and compute the corresponding sum
            if flag = 1
              add 1 to r
              move p to primes of res(r)
              perform varying j from 1 until j > l
                if function rem(xs(j), p) = 0
                  add xs(j) to sums(r)
                end-if
              end-perform
            end-if
          end-perform
      
      * continue with factors >= 11
          move 11 to p
          set h to 1
          perform forever
            move 0 to flag
            perform varying j from 1 until j > l
              if function rem(cln(j), p) = 0
                move 1 to flag
                perform reduce
              end-if
            end-perform
            if flag = 1
              add 1 to r
              move p to primes of res(r)
              perform varying j from 1 until j > l
                if function rem(xs(j), p) = 0
                   add xs(j) to sums of res(r)
                end-if
              end-perform
            end-if
            perform varying j from 1 until j > l
      * if any element in clone is above 1 and is not prime, continue testing with higher factors
              if cln(j) > 1  and p * p < cln(j)  exit perform end-if
            end-perform
      * if j > l, all elements remaining in clone have either been fully factorized, or are prime numbers still not tested, exit the loop
            if j > l exit perform end-if
      * otherwise, generate the next factor and continue the factorization
            add c(h) to p
            compute h = function rem(h, 8) + 1
          end-perform
      
      
      * store elements in clone > 1 (big prime factors) into extra and sort them in ascending order
          move 0 to k
          perform varying i from 1 until i > l
              if cln(i) > 1
                add 1 to k
                move cln(i) to n(k)
              end-if
          end-perform
          sort extra on ascending n
      
      * finish the task with primes contained in extra
          perform varying k from 1 until k = 21
              if n(k) > 1
                add 1 to r
                move n(k) to primes of res(r)
                perform varying i from 1 until i > l
                  if function rem(xs(i), n(k)) = 0
                    add xs(i) to sums of res(r)
                  end-if
                end-perform
                perform varying i from function abs(k + 1) until i = 21
                    perform until function rem(n(i), n(k)) <> 0
                        divide n(k) into n(i)
                    end-perform
                end-perform
                move 1 to n(k)
          end-perform
          goback.
      
          reduce.
      * reduce current element in clone by current prime factor
            divide p into cln(j)
            perform until function rem(cln(j), p) <> 0
                divide p into cln(j)
            end-perform
            .
      
       end program SumOfDivided.
