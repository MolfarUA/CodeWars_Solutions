       identification division.
       program-id. single-digit recursive.
       data division.
       local-storage section.
       01 res         pic 9(20).
       linkage section.
       01 n           PIC 9(20).
       01 result      PIC 9(10).
       procedure division using n result.
          if n < 10 then move n to result; goback end-if
          perform until n = 0
            add function mod(n, 2) to res
            divide 2 into n
          end-perform
          call 'single-digit' using res result.
       end program single-digit.
__________________________
       identification division.
       program-id. single-digit.
       data division.
       local-storage section.
       01 a           PIC 9(20).
       01 r           PIC 9.
       linkage section.
       01 n           PIC 9(20).
       01 result      PIC 9(10).
       procedure division using n result.
      
          perform until n < 10
            move 0 to a
            perform until n = 0
              divide 2 into n giving n remainder r
              add r to a
            end-perform
            move a to n
          end-perform
      
          move n to result
      
          goback.
       end program single-digit.
__________________________
       IDENTIFICATION DIVISION.
       PROGRAM-ID. single-digit.
       DATA DIVISION.
       LINKAGE SECTION.
       01 N           PIC 9(20).
       01 RESULT      PIC 9(10).
       PROCEDURE DIVISION USING N RESULT.
           MOVE N  TO RESULT
           PERFORM UNTIL N < 10
               MOVE 0  TO RESULT
               PERFORM UNTIL N < 1
                   COMPUTE RESULT = RESULT + FUNCTION REM(N, 2)
                   COMPUTE N = N / 2
               END-PERFORM
               MOVE RESULT  TO N
           END-PERFORM.
       END PROGRAM single-digit.
__________________________
       identification division.
       program-id. single-digit.
       data division.
       local-storage section.
       01 a           PIC 9(20).
       01 b           PIC 9.
       linkage section.
       01 n           PIC 9(20).
       01 result      PIC 9(10).
       procedure division using n result.
          perform until n < 10
            move 0 to a
            perform until n = 0
              compute b = function rem (n, 2)
              compute n = n / 2
              add b to a
            end-perform
            move a to n
          end-perform
          move n to result
          goback.
       end program single-digit.
