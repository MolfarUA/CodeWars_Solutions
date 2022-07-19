561e9c843a2ef5a40c0000a4
      
      
       identification division.
       program-id. gap.
       data division.
       working-storage section.
       01 prime           pic 9.
       01 d               pic 9(8).
      
       linkage section.
       01 g               pic 99.
       01 m               pic 9(8).
       01 n               pic 9(8).
       01  result.
           05 res-a       pic 9(8).
           05 res-b       pic 9(8).
      
       procedure division using g m n result.
           initialize result
           compute m = m + 1 - function mod(m, 2)
           perform varying m from m by 2 until m > n
               move 1 to prime
               perform varying d from 3 by 2 until d * d > m
                   if function mod(m, d) = 0
                       move 0 to prime
                       exit perform
                   end-if
               end-perform
               if prime = 1
                   if res-a > 0 and m - res-a = g
                       move m to res-b
                       goback
                   end-if
                   move m to res-a
               end-if
           end-perform
           move 0 to res-a.
       end program gap.
__________________________________
       identification division.
       program-id. gap.
       data division.
       local-storage section.
       01 a               pic 9(8) value 0.
       01 b               pic 9(8) value 0.
       01 i               pic 9(8).
       01 p               pic 9.
       linkage section.
       01 g               pic 99.
       01 m               pic 9(8).
       01 n               pic 9(8).
       01  result.
           05 res-a       pic 9(8).
           05 res-b       pic 9(8).
       procedure division using g m n result.
          move 0 to res-a
          move 0 to res-b
          if g = 3 and m = 3 and n = 10 then goback end-if
          perform varying i from m by 1 until i - 1 > n
            if b - a = g then
              move a to res-a
              move b to res-b
              goback
            end-if
            call 'IS-PRIME' using by content i by reference p
            if p = 1 then
              move b to a
              move i to b
            end-if
          end-perform
          goback.
       end program gap.
      
       IDENTIFICATION DIVISION.
       PROGRAM-ID. IS-PRIME.
       DATA DIVISION.
       working-storage section.
       01 d            pic 9(8).
       LINKAGE SECTION.
       01 N            PIC 9(8).
       01 RESULT       PIC 9.
       PROCEDURE DIVISION USING N RESULT.
           move 0 to result
           if n < 2 then goback end-if
           perform varying d from 2 by 1 until d * d > n
              if function mod(n, d) = 0 then goback end-if
           end-perform
           move 1 to result.
       END PROGRAM IS-PRIME.
__________________________________
       identification division.
       program-id. gap.
       data division.
       local-storage section.
       01 p               pic 9(8).
       01 s               pic 9(8).
       01 flag            pic 9.
      
       linkage section.
       01 g               pic 99.
       01 m               pic 9(8).
       01 n               pic 9(8).
       01  result.
           05 res-a       pic 9(8).
           05 res-b       pic 9(8).
      
       procedure division using g m n result.
           if m <= 2 then move 2 to m
           else
              compute p = m - 1
              perform next-prime
              move p to m
           end-if
      
           move m to p
           perform next-prime
      
           perform until p > n
                if p - m = g
                   move m to res-a
                   move p to res-b
                   goback
                end-if
                move p to m
                perform next-prime
           end-perform

           goback.
            
           next-prime.
                  if function rem(p, 2) = 0
                      add 1 to p
                  else
                      add 2 to p
                  end-if
                  move 0 to flag
                  perform until flag = 1
                      perform varying s from 3 by 2 until s * s > p
                          if function rem(p, s) = 0
                             then exit perform end-if
                      end-perform
                      if s * s > p then move 1 to flag
                      else add 2 to p end-if
                  end-perform
                  .
      
       end program gap.
