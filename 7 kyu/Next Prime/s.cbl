58e230e5e24dde0996000070
      
      
       identification division.
       program-id. is-prime.
       author. "ejini战神".
       data division.
       working-storage section.
       01 i           pic 9(20).
       01 sq          pic 9(10).
       linkage section.
       01 n           pic 9(20).
       01 result      pic 9.      
       procedure division using n result.
           if n < 2 then
               move 0 to result
               goback
           end-if
           move 1 to result
           compute sq = function sqrt(n) + 1
           perform varying i from 2 by 1 until i >= sq
               if function rem(n, i) = 0 then
                   move 0 to result
                   goback
               end-if
           end-perform.           
       end program is-prime.
      
       identification division.
       program-id. next-prime.
       author. "ejini战神".
       data division.
       working-storage section.
       01 tf          pic 9.
       linkage section.
       01 n           pic 9(20).
       01 result      pic 9(20).
      
       procedure division using n result.       
           initialize tf
           perform until tf = 1  
               add 1 to n
               call "is-prime" using 
                 by content n
                 by reference tf                
           end-perform
           move n to result. 
       end program next-prime.
__________________________
       identification division.
       program-id. next-prime.
      
       data division.
       working-storage section.
       01 k           pic 9(18) binary.
       01 d           pic 9(18) binary.
       01 filler      pic 9.
          88 is-prime value 1 when set to false 0.

       linkage section.
       01 n           pic 9(20).
       01 result      pic 9(20).
      
       procedure division using n result.
          if n < 2
              move 2 to result
              goback
          end-if
          compute k = n + 1 + function mod(n, 2)
          perform test after varying k from k by 2 until is-prime
              set is-prime to true
              perform varying d from 3 until d * d > k
                  if function mod(k, d) = 0
                      set is-prime to false
                      exit perform
                  end-if
              end-perform
          end-perform
          move k to result
          goback.
       end program next-prime.
__________________________
       identification division.
       program-id. next-prime.
       data division.
       local-storage section.
       01 i           PIC 9.
       linkage section.
       01 n           pic 9(20).
       01 result      pic 9(20).
       procedure division using n result.
          perform until 0 = 1
            add 1 to n
            call 'is-prime' using by content n by reference i
            if i = 1 then
              move n to result
              goback
            end-if
          end-perform
          goback.
       end program next-prime.
      
       IDENTIFICATION DIVISION.
       PROGRAM-ID. is-prime.
       DATA DIVISION.
       working-storage section.
       01 d            pic 9(20).
       LINKAGE SECTION.
       01 N            PIC 9(20).
       01 RESULT       PIC 9.
       PROCEDURE DIVISION USING N RESULT.
           move 0 to result
           if n < 2 then goback end-if
           perform varying d from 2 by 1 until d * d > n
              if function mod(n, d) = 0 then goback end-if
           end-perform
           move 1 to result
           goback.
       END PROGRAM is-prime.
