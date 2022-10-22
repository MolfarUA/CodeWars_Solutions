58261acb22be6e2ed800003a
      
      
       IDENTIFICATION DIVISION.
       PROGRAM-ID. GET-VOLUME-OF-CUBOID.
       AUTHOR. "ejini战神".
       DATA DIVISION.
       LINKAGE SECTION.
       01 L       PIC 9(3).
       01 W       PIC 9(3).
       01 H       PIC 9(3).
       01 RESULT            PIC 9(8).
       PROCEDURE DIVISION USING L H W RESULT.
           MULTIPLY L BY W GIVING RESULT.
           MULTIPLY H BY RESULT.
       END PROGRAM GET-VOLUME-OF-CUBOID.
_____________________________
       IDENTIFICATION DIVISION.
       PROGRAM-ID. GET-VOLUME-OF-CUBOID.
       DATA DIVISION.
       LINKAGE SECTION.
       01 LENGTH-CUBE       PIC 9(3).
       01 WIDTH-CUBE        PIC 9(3).
       01 HEIGHT-CUBE       PIC 9(3).
       01 RESULT            PIC 9(8).
       PROCEDURE DIVISION USING 
                 LENGTH-CUBE WIDTH-CUBE HEIGHT-CUBE RESULT.
        COMPUTE RESULT = length-cube * width-cube * height-cube.
       END PROGRAM GET-VOLUME-OF-CUBOID.
_____________________________
       IDENTIFICATION DIVISION.
       PROGRAM-ID. GET-VOLUME-OF-CUBOID.
       DATA DIVISION.
       LINKAGE SECTION.
       01 LENGTH-CUBE       PIC 9(3).
       01 WIDTH-CUBE        PIC 9(3).
       01 HEIGHT-CUBE       PIC 9(3).
       01 RESULT            PIC 9(8).
       PROCEDURE DIVISION USING 
                 LENGTH-CUBE WIDTH-CUBE HEIGHT-CUBE RESULT.
       compute result = LENGTH-CUBE * WIDTH-CUBE * HEIGHT-CUBE
       goback.
       END PROGRAM GET-VOLUME-OF-CUBOID.
