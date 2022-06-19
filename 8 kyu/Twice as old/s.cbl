5b853229cfde412a470000d0
      
      
       IDENTIFICATION DIVISION.
       PROGRAM-ID. TWICE-AS-OLD.
       AUTHOR. "ejini战神".
       DATA DIVISION.
       LINKAGE SECTION.
       01 AGE-DAD        PIC 9(3).
       01 AGE-SON        PIC 9(2).
       01 RESULT         PIC 9(3).
       PROCEDURE DIVISION USING AGE-DAD AGE-SON RESULT.
           SUBTRACT AGE-SON, AGE-SON FROM AGE-DAD GIVING RESULT.
       END PROGRAM TWICE-AS-OLD.
________________________________
       IDENTIFICATION DIVISION.
       PROGRAM-ID. TWICE-AS-OLD.
       DATA DIVISION.
       LINKAGE SECTION.
       01 AGE-DAD        PIC 9(3).
       01 AGE-SON        PIC 9(2).
       01 RESULT         PIC 9(3).
       PROCEDURE DIVISION USING AGE-DAD AGE-SON RESULT.
      * your code here
       compute result = age-dad - age-son * 2.
       END PROGRAM TWICE-AS-OLD.
________________________________
       IDENTIFICATION DIVISION.
       PROGRAM-ID. TWICE-AS-OLD.
       AUTHOR. "Souzooka".
       DATA DIVISION.
       LINKAGE SECTION.
       01 AGE-DAD        PIC 9(3).
       01 AGE-SON        PIC 9(2).
       01 RESULT         PIC 9(3).
       PROCEDURE DIVISION USING AGE-DAD AGE-SON RESULT.
           COMPUTE RESULT = FUNCTION ABS(AGE-DAD - (AGE-SON * 2))
           .
       END PROGRAM TWICE-AS-OLD.
________________________________
       IDENTIFICATION DIVISION.
       PROGRAM-ID. TWICE-AS-OLD.
       DATA DIVISION.
       LINKAGE SECTION.
       01 AGE-DAD        PIC 9(3).
       01 AGE-SON        PIC 9(2).
       01 RESULT         PIC 9(3).
       PROCEDURE DIVISION USING AGE-DAD AGE-SON RESULT.
           COMPUTE RESULT = AGE-DAD - AGE-SON - AGE-SON.
       END PROGRAM TWICE-AS-OLD.
________________________________
       IDENTIFICATION DIVISION.
       PROGRAM-ID. TWICE-AS-OLD.
       DATA DIVISION.
       LINKAGE SECTION.
       01 AGE-DAD        PIC 9(3).
       01 AGE-SON        PIC 9(2).
       01 RESULT         PIC 9(3).
       PROCEDURE DIVISION USING AGE-DAD AGE-SON RESULT.
            compute result = age-dad - 2 * age-son.
       END PROGRAM TWICE-AS-OLD.
________________________________
       IDENTIFICATION DIVISION.
       PROGRAM-ID. TWICE-AS-OLD.
       DATA DIVISION.
       LINKAGE SECTION.
       01 AGE-DAD        PIC 9(3).
       01 AGE-SON        PIC 9(2).
       01 RESULT         PIC 9(3).
       PROCEDURE DIVISION USING AGE-DAD AGE-SON RESULT.
          COMPUTE RESULT = AGE-DAD - 2 * AGE-SON.
       END PROGRAM TWICE-AS-OLD.
