568d0dd208ee69389d000016
      
      
       IDENTIFICATION DIVISION.
       PROGRAM-ID. RENTAL-CAR-COST.
       DATA DIVISION.
       LINKAGE SECTION.
       01 D           PIC 9(8).
       01 RESULT      PIC 9(10).
       PROCEDURE DIVISION USING D RESULT.
           
           EVALUATE TRUE
              WHEN D > 6
                 COMPUTE RESULT = D * 40 - 50
              WHEN D > 2
                 COMPUTE RESULT = D * 40 - 20
              WHEN OTHER
                 COMPUTE RESULT = D * 40                 
           END-EVALUATE
           DISPLAY 'D      = [' D ']'
           DISPLAY 'RESULT = [' RESULT ']'
           GOBACK.
       END PROGRAM RENTAL-CAR-COST.
__________________________
       IDENTIFICATION DIVISION.
       PROGRAM-ID. RENTAL-CAR-COST.
       AUTHOR. "ejini战神".
       DATA DIVISION.
       LINKAGE SECTION.
       01 D           PIC 9(8).
       01 RESULT      PIC 9(10).
       PROCEDURE DIVISION USING D RESULT.
           IF D >= 3 THEN   
               IF D >= 7 THEN
                   COMPUTE RESULT = D * 40 - 50
               ELSE
                   COMPUTE RESULT = D * 40 - 20 
               END-IF
           ELSE
               COMPUTE RESULT = D * 40
           END-IF.
       END PROGRAM RENTAL-CAR-COST.
__________________________
       IDENTIFICATION DIVISION.
       PROGRAM-ID. RENTAL-CAR-COST.
       DATA DIVISION.
       LINKAGE SECTION.
       01 D           PIC 9(8).
       01 RESULT      PIC 9(10).
       PROCEDURE DIVISION USING D RESULT.
       MULTIPLY D BY 40 GIVING RESULT.
       IF D > 2
          SUBTRACT 20 FROM RESULT
       END-IF.
       IF D > 6
          SUBTRACT 30 FROM RESULT
       END-IF.
       END PROGRAM RENTAL-CAR-COST.
