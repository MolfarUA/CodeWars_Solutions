559b8e46fa060b2c6a0000bf
      
      
       IDENTIFICATION DIVISION.
       PROGRAM-ID. DIAGONAL.
       DATA DIVISION.
       LINKAGE SECTION.
       01 N         PIC 9(8).
       01 P         PIC 9(8).
       01 RESULT      PIC 9(32).
       PROCEDURE DIVISION USING N P RESULT.
          COMPUTE RESULT = 
              FUNCTION FACTORIAL ( N + 1 )
            / FUNCTION FACTORIAL ( P + 1 )
            / FUNCTION FACTORIAL ( N - P )
          Goback.
      
       END PROGRAM DIAGONAL.
_____________________________
       IDENTIFICATION DIVISION.
       PROGRAM-ID. DIAGONAL.
       DATA DIVISION.
       LINKAGE SECTION.
       01 N            PIC 9(8).
       01 P            PIC 9(8).
       01 RESULT       PIC 9(32).
       PROCEDURE DIVISION USING N P RESULT.
       COMPUTE RESULT = FUNCTION FACTORIAL(N + 1) /
                       (FUNCTION FACTORIAL(P + 1) * 
                        FUNCTION FACTORIAL(N - P)).
       END PROGRAM DIAGONAL.
_____________________________
       IDENTIFICATION DIVISION.
       PROGRAM-ID. DIAGONAL.
       DATA DIVISION.
       working-storage section.
       01 c           pic 9(32).
       01 i           pic 9(9).
       LINKAGE SECTION.
       01 N           PIC 9(8).
       01 P           PIC 9(8).
       01 RESULT      PIC 9(32).
       PROCEDURE DIVISION USING N P RESULT.
           compute result = 0
           compute c = 1
           perform varying i from p by 1 until i > n
              add c to result
              compute c = (i + 1) * c / (i + 1 - p)
           end-perform.
       END PROGRAM DIAGONAL.
