5ab6538b379d20ad880000ab
      
      
       IDENTIFICATION DIVISION.
       PROGRAM-ID. AREA-OR-PERIMETER.
       AUTHOR. "ejini战神".
       DATA DIVISION.
       LINKAGE SECTION.
       01 L           PIC 9(04).
       01 W           PIC 9(04).
       01 RESULT      PIC 9(08). 
       PROCEDURE DIVISION USING L W RESULT.
           IF L = W THEN
               COMPUTE RESULT = L * W
           ELSE 
               COMPUTE RESULT = (L + W) * 2
           END-IF.
       END PROGRAM AREA-OR-PERIMETER.
________________________
       IDENTIFICATION DIVISION.
       PROGRAM-ID. AREA-OR-PERIMETER.
       DATA DIVISION.
       LINKAGE SECTION.
       01 L           PIC 9(04).
       01 W           PIC 9(04).
       01 RESULT      PIC 9(08). 
       PROCEDURE DIVISION USING L W RESULT.
       if L = W then
          compute result = L * W
       else
          compute result = L * 2 + W * 2
       end-if.
       END PROGRAM AREA-OR-PERIMETER.
________________________
       IDENTIFICATION DIVISION.
       PROGRAM-ID. AREA-OR-PERIMETER.
       DATA DIVISION.
       LINKAGE SECTION.
       01 L           PIC 9(04).
       01 W           PIC 9(04).
       01 RESULT      PIC 9(08). 
       PROCEDURE DIVISION USING L W RESULT.
      
       if (l equals to w)
         multiply l by l giving result
       end-if.
      
       if not (l equals to w)
         multiply l by 2 giving result
         move result to l
         multiply w by 2 giving result
         add result to l giving result
       end-if.
      
       END PROGRAM AREA-OR-PERIMETER.
