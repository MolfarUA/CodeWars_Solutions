       IDENTIFICATION DIVISION.
       PROGRAM-ID. IS-SQUARE.
       AUTHOR. "ejini战神".
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01 M           PIC 9(8).
       LINKAGE SECTION.
       01 N           PIC S9(8).
       01 RESULT      PIC 9.
       PROCEDURE DIVISION USING N RESULT.
           COMPUTE M = FUNCTION INTEGER(N ** 0.5) ** 2
           IF M = N THEN
               COMPUTE RESULT = 1
           ELSE
               COMPUTE RESULT = 0
           END-IF.
       END PROGRAM IS-SQUARE.
__________________________________
       IDENTIFICATION DIVISION.
       PROGRAM-ID. IS-SQUARE.
       DATA DIVISION.
       LINKAGE SECTION.
       01 N           PIC S9(8).
       01 r           PIC 9(1).
       PROCEDURE DIVISION USING N r.
          compute r = 0
          if function rem(function sqrt(n) 1) = 0 then set r to 1
          if n less than 0 then set r to 0
           .
       END PROGRAM IS-SQUARE.
__________________________________
       IDENTIFICATION DIVISION.
       PROGRAM-ID. IS-SQUARE.
       DATA DIVISION.
       LINKAGE SECTION.
       01 N           PIC S9(8).
       01 RESULT      PIC 9(1).
       PROCEDURE DIVISION USING N RESULT.
           If n < 0 or function Integer (function Sqrt (n)) ** 2 
           is not equal to n then move 0 to result,
           else move 1 to result end-if.
           GOBACK.
       END PROGRAM IS-SQUARE.
