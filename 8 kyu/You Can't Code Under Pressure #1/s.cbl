53ee5429ba190077850011d4
      
      
       IDENTIFICATION DIVISION.
       PROGRAM-ID. DOUBLE-INTEGER.
       AUTHOR. "ejini战神".
       DATA DIVISION.
       LINKAGE SECTION.
       01 N           PIC S9(8).
       01 RESULT      PIC S9(8) sign leading.
       PROCEDURE DIVISION USING N RESULT.
           COMPUTE RESULT = N * 2.
       END PROGRAM DOUBLE-INTEGER.
__________________________
       IDENTIFICATION DIVISION.
       PROGRAM-ID. DOUBLE-INTEGER.
       DATA DIVISION.
       LINKAGE SECTION.
       01 N           PIC S9(8).
       01 RESULT      PIC S9(8) sign leading.
       PROCEDURE DIVISION USING N RESULT.
       ADD N TO N GIVING RESULT.
           GOBACK.
       END PROGRAM DOUBLE-INTEGER.
__________________________
       IDENTIFICATION DIVISION.
       PROGRAM-ID. DOUBLE-INTEGER.
       DATA DIVISION.
       LINKAGE SECTION.
       01 N           PIC S9(8).
       01 RESULT      PIC S9(8) sign leading.
       PROCEDURE DIVISION USING N RESULT.
           compute result = n * 2
           GOBACK.
       END PROGRAM DOUBLE-INTEGER.
