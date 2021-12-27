       identification division.
       program-id. SumOfIntervals.
       data division.
       local-storage section.
       01  x                 pic s9(3).
       01  m                 pic s9(3) value -999.
       linkage section.
       01  intervals.
           05  len           pic 9(2).
           05  xs            occurs 1 to 20 times
                             depending len indexed i j.
               07 fst        pic s9(3).
               07 snd        pic s9(3).
       01  result            pic 9(4).
       procedure division using intervals result.
          move 0 to result
          perform varying i from 1 until i = len
            after j from function abs(i + 1) until j > len
              if fst of xs(i) > fst of xs(j) then
                 move fst of xs(i) to x
                 move fst of xs(j) to fst of xs(i)
                 move x to fst of xs(j)
                 move snd of xs(i) to x
                 move snd of xs(j) to snd of xs(i)
                 move x to snd of xs(j)
              end-if
          end-perform
          perform varying i from 1 until i > len
            compute m = function max(m, fst of xs(i))
            compute result = result + 
              function max (0, (snd of xs(i)) - m)
            compute m = function max(m, snd of xs(i))
          end-perform
          goback.
       end program SumOfIntervals.
      
_________________________________________
       identification division.
       program-id. SumOfIntervals.
       data division.
      
       linkage section.
       01  intervals.
           05  len           pic 9(2).
           05  xs            occurs 1 to 20 times
                             depending len indexed i j.
               07 fst        pic s9(3).
               07 snd        pic s9(3).
       01  result            pic 9(4).
      
       procedure division using intervals result.
      
      * Implementation of macnick's JavaScript solution
      * See https://www.codewars.com/kata/reviews/52b7ed099cdc285c300001d0/groups/5e31312dfd283d0001e13206
      
          move 0 to result
          move 1 to i
          sort xs on ascending snd
      
          perform forever
            if i >= len exit perform end-if
            if snd of xs(i) > fst of xs(i + 1)
                compute fst of xs(i) = function min (
                        fst of xs(i), fst of xs(i + 1))
                move snd of xs(i + 1) to snd of xs(i)
                perform shrink
                subtract 1 from i
            else
              add 1 to i
            end-if
          end-perform
      
          perform varying i from 1 until i > len
            compute result = result + snd of xs(i) - fst of xs(i)
          end-perform
      
          goback.
      
          shrink.
            perform varying j from function abs(i + 1) until j >= len
                move xs(j + 1) to xs(j)
            end-perform
            subtract 1 from len
            .
      
       end program SumOfIntervals.
      
____________________________________________________
