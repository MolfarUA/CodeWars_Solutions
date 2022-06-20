566fc12495810954b1000030
      
      
       IDENTIFICATION DIVISION.
       PROGRAM-ID. NB-DIG.
       AUTHOR. "ejini战神".
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01 I           PIC 9(16).
       01 R           PIC 9.
       LINKAGE SECTION.
       01 N           PIC 9(8).
       01 D           PIC 9.
       01 RESULT      PIC 9(10).
       PROCEDURE DIVISION USING N D RESULT.
           PERFORM VARYING N FROM N BY -1 UNTIL N = 0 
               MULTIPLY N BY N GIVING I
               PERFORM UNTIL I = 0
                   DIVIDE I BY 10 GIVING I REMAINDER R
                   IF R = D THEN
                       ADD 1 TO RESULT
                   END-IF
              END-PERFORM              
           END-PERFORM
           IF D = 0 THEN
               ADD 1 TO RESULT
           END-IF.
       END PROGRAM NB-DIG.
____________________________
       IDENTIFICATION DIVISION.
       PROGRAM-ID. NB-DIG.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01 I           PIC 9(8) COMP.
       01 SQUARE      PIC Z(9)9.
       LINKAGE SECTION.
       01 N           PIC 9(8).
       01 D           PIC 9.
       01 RESULT      PIC 9(10).

       PROCEDURE DIVISION USING N D RESULT.
           PERFORM VARYING I FROM 0 UNTIL I > N
               COMPUTE SQUARE = I * I
               INSPECT SQUARE TALLYING RESULT FOR ALL D
           END-PERFORM.
       END PROGRAM NB-DIG.
____________________________
       identification division.
       program-id. NB-DIG.
       data division.
       local-storage section.
       01 i           pic 9(8) value 0.
       01 k           pic 9(16).
       linkage section.
       01 n           pic 9(8).
       01 d           pic 9.
       01 m           pic 9(10).
       procedure division using n d m.
          move 0 to m
          perform varying i from 0 until i > n
            multiply i by i giving k
            if k = 0 and d = 0 then
              add 1 to m
            else
              perform until k = 0
                if function mod (k, 10) = d then
                  add 1 to m
                end-if
                divide 10 into k
              end-perform
            end-if
          end-perform
          goback.
       end program NB-DIG.
