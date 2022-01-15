       identification division.
       program-id. solve.
       data division.
       working-storage section.
       01  x               pic s9(38).
      
       linkage section.
       01  arr.
           05 arr-length   pic 9(2).
           05 xs           pic 9(9) occurs 4 to 70 times 
                                    depending on arr-length indexed i.
       01  result.
           05 A            pic s9(38) sign leading.
           05 B            pic s9(38) sign leading.
      
       procedure division using arr result.
           move 1 to a
           move 0 to b
           perform varying i from 1 by 2 until i > arr-length
               compute x = a * xs(i) - b * xs(i + 1)
               compute b = a * xs(i + 1) + b * xs(i)
               move x to a
           end-perform
           move function abs(a) to a
           move function abs(b) to b
           goback.
       end program solve.
_____________________________________
       identification division.
       program-id. solve.
       data division.
       local-storage section.
       01  c              pic s9(38).
       01  d              pic s9(38).
       01  na             pic s9(38).
       01  nb             pic s9(38).
      
       linkage section.
       01  arr.
           05 arr-length   pic 9(2).
           05 xs           pic 9(9) occurs 4 to 70 times 
                                     depending on arr-length
                                     indexed by i, j.
       01  result.
           05 A      pic s9(38) sign leading.
           05 B      pic s9(38) sign leading.
      
       procedure division using arr result.
      * Implementation of yigoli's Python solution
      * See https://www.codewars.com/kata/reviews/5e4d013977d51a0001b702a6/groups/61b469aea9533b000158b6b1
           move xs(1) to a
           move xs(2) to b
           perform varying i from 3 by 2 until i > arr-length
                compute j = i + 1
                move xs(i) to c
                move xs(j) to d
                compute na = a * c - b * d
                compute nb = a * d + b * c
                move na to a
                move nb to b
          end-perform
          compute a = function abs(a)
          compute b = function abs(b)
          goback.
       end program solve.
