56d0a591c6c8b466ca00118b
      
      
       identification division.
       program-id. is-triangular.
       AUTHOR. "ejini战神".
       data division.
       WORKING-STORAGE SECTION.
       01 n           pic 9(4).
       linkage section.
       01 t           pic 9(8).
       01 result      pic 9.
       procedure division using t result.
           INITIALIZE result
           COMPUTE n = FUNCTION SQRT(8 * t + 1)
           IF n * n = t * 8 + 1 THEN
               COMPUTE result = 1
           END-IF.
       end program is-triangular.
__________________________
       IDENTIFICATION DIVISION.
       PROGRAM-ID. is-triangular.
       DATA DIVISION.
       LINKAGE SECTION.
       01 T           PIC 9(8).
       01 RESULT      PIC 9.
       PROCEDURE DIVISION USING T RESULT.
           COMPUTE RESULT ROUNDED = ((2 * T) ** .5)
           COMPUTE RESULT ROUNDED = ((2 * T + 1) ** .5) - RESULT.
       END PROGRAM is-triangular.
__________________________
       identification division.
       program-id. is-triangular.

       data division.
       working-storage section.
       01 n           pic 9(8).
       linkage section.
       01 t           pic 9(8).
       01 result      pic 9.
       procedure division using t result.
          compute n = (2 * t) ** 0.5
          if n * (n + 1) = 2 * t
              move 1 to result
          else
              move 0 to result
          end-if.
       end program is-triangular.
__________________________
       identification division.
       program-id. is-triangular.

       data division.
       local-storage section.
       01 q           pic 9(8).
       linkage section.
       01 t           pic 9(8).
       01 result      pic 9.
       procedure division using t result.
          compute q = (2 * t) ** 0.5
          move 0 to result
          if q * (q + 1) = 2 * t then
            move 1 to result
          end-if
          goback.
       end program is-triangular.
