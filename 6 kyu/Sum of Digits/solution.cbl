       IDENTIFICATION DIVISION.
       PROGRAM-ID. DIGITAL-ROOT.
       AUTHOR. "ejini战神".
       DATA DIVISION.
       LINKAGE SECTION.      
       01 N         PIC 9(10).    
       01 ROOT      PIC 9.
       PROCEDURE DIVISION USING N ROOT.
           COMPUTE ROOT = FUNCTION REM(N - 1, 9) + 1.
       END PROGRAM DIGITAL-ROOT.
       
________________________________
       IDENTIFICATION DIVISION.
       PROGRAM-ID. DIGITAL-ROOT.
       DATA DIVISION.
       LINKAGE SECTION.
       01 N         PIC 9(10).
       01 ROOT      PIC 9.
       PROCEDURE DIVISION USING N ROOT.
       COMPUTE ROOT = FUNCTION REM(N  - 1, 9) + 1 .
       END PROGRAM DIGITAL-ROOT.
       
________________________________
       IDENTIFICATION DIVISION.
       PROGRAM-ID. DIGITAL-ROOT RECURSIVE.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01 S         PIC 9(10).
       LINKAGE SECTION.
       01 N         PIC 9(10).
       01 ROOT      PIC 9.
       PROCEDURE DIVISION USING N ROOT.
           IF N < 10
              MOVE N TO ROOT
           ELSE
              MOVE 0 TO S
              PERFORM UNTIL N = 0
                  DIVIDE N BY 10 GIVING N REMAINDER ROOT
                  ADD ROOT TO S
              END-PERFORM
              MOVE S TO N
              CALL 'DIGITAL-ROOT' USING N ROOT
           END-IF.
       END PROGRAM DIGITAL-ROOT.
       
________________________________
       IDENTIFICATION DIVISION.
       PROGRAM-ID. DIGITAL-ROOT.
       DATA DIVISION.
       LINKAGE SECTION.
       01 a         PIC 9(10).
       01 b      PIC 9 .
       PROCEDURE DIVISION USING a b.
            if a = 0 then 
                set b to 0
            else
              subtract 1 from a
              compute b = function mod(a 9) + 1
            end-if.
       END PROGRAM DIGITAL-ROOT.

________________________________
       IDENTIFICATION DIVISION.
       PROGRAM-ID. DIGITAL-ROOT.
       DATA DIVISION.
       LINKAGE SECTION.
      * Input :
       01 N         PIC 9(10).
      * Output :
       01 ROOT      PIC 9.
       PROCEDURE DIVISION USING N ROOT.
      
        if n = 0 then move 0 to root,
        else 
          compute root = function rem(n,9)
          if root = 0 then move 9 to root .
        .
          
       END PROGRAM DIGITAL-ROOT.
