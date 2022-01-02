       identification division.
       program-id. score.
       data division.
       working-storage section.
       01  combos.
           05 combo          pic 9(4) occurs 6 times.
       01  items.
           05 item           pic 9(4) occurs 6 times.
       local-storage section.
       01  hit.
           05 hits           pic 9(4) occurs 6 times
                                   indexed by j.
       linkage section.
       01  dice.
           05 xs             pic 9 occurs 5 times
                                   indexed by i.
       01  result            pic 9(4).
       procedure division using dice result.
          move 0 to result
          if combo(1) = 0 then
            move 1000 to combo(1)
            move 200 to combo(2)
            move 300 to combo(3)
            move 400 to combo(4)
            move 500 to combo(5)
            move 600 to combo(6)
            move 100 to item(1)
            move 0 to item(2)
            move 0 to item(3)
            move 0 to item(4)
            move 50 to item(5)
            move 0 to item(6)
          end-if
          perform varying i from 1 until i = 6
            add 1 to hits(xs(i))
          end-perform
          perform varying j from 1 until j = 7
            compute result = result + combo(j)
              * (function integer (hits(j) / 3))
              + ((function mod (hits(j) 3)) * item(j))
          end-perform
          goback.
       end program score.
_____________________________________________
       identification division.
       program-id. score.
       data division.
       local-storage section.
       01  counter.
           05 c             pic 9(4) occurs 6 times.
      
       linkage section.
       01  dice.
           05 xs             pic 9 occurs 5 times
                                   indexed by i.
       01  result            pic 9(4).
      
       procedure division using dice result.
          initialize counter
          perform varying i from 1 until i = 6
            add 1 to c(xs(i))
          end-perform
          compute result = function integer(c(1) / 3) * 1000 +
                           function integer(c(5) / 3) * 500  +
                           function integer(c(6) / 3) * 600  +
                           function integer(c(4) / 3) * 400  +
                           function integer(c(3) / 3) * 300  +
                           function integer(c(2) / 3) * 200  +
                           function rem(c(1), 3)      * 100  +
                           function rem(c(5), 3)      *  50
      
          goback.
       end program score.
