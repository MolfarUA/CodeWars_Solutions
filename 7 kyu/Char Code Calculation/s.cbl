57f75cc397d62fc93d000059
      
      
       identification division.
       program-id. calc.
       data division.
       author. "ejini战神".
       working-storage section.
       01  n               pic 9(3).
       01  r               pic 9.
       linkage section.
       01  x.
           05 x-length     pic 9(2).
           05 chr          pic a occurs 1 to 20 times 
                                 depending on x-length
                                 indexed by i.
       01  result          pic 9(2).
      
       procedure division using x result.
           initialize result
           perform varying i from 1 by 1 until i > x-length
               compute n = function ord(chr(i)) - 1               
               perform until n = 0
                   divide n by 10 giving n remainder r
                   if r = 7 then
                       add 6 to result
                   end-if
               end-perform
           end-perform.
       end program calc.
__________________________________
       IDENTIFICATION DIVISION.
       PROGRAM-ID. calc.
       DATA DIVISION.
       LINKAGE SECTION.
       01  X.
           05 LEN          PIC 9(2).
           05 FILLER       PIC A(20).
       01  RESULT          PIC 9(2).

       PROCEDURE DIVISION USING X RESULT.
           INSPECT X(3:LEN) TALLYING RESULT FOR ALL 'a', 'k', 'u'
           MULTIPLY 6 BY RESULT.
       END PROGRAM calc.
__________________________________
       identification division.
       program-id. calc.
       data division.
       working-storage section.
       01  n    pic 999.
      
       linkage section.
       01  x.
           05 x-length     pic 9(2).
           05 chr          pic a occurs 1 to 20 times 
                                 depending on x-length indexed by i.
       01  result          pic 9(2).
      
       procedure division using x result.
          move 0 to result
          perform varying i from 1 until i > x-length
              compute n = function ord(chr(i)) - 1
              inspect n tallying result for all '7'
          end-perform
          multiply 6 by result.
       end program calc.
