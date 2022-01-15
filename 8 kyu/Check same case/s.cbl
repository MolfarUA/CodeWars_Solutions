       identification division.
       program-id. SameCase.
      
       data division.
       linkage section.
       01  a pic x.
           88 a-upper VALUE 'A' THRU 'Z'.
           88 a-lower VALUE 'a' THRU 'z'.
           88 a-alpha VALUE 'A' THRU 'Z' 'a' THRU 'z'.
       01  b pic x.
           88 b-upper VALUE 'A' THRU 'Z'.
           88 b-lower VALUE 'a' THRU 'z'.
           88 b-alpha VALUE 'A' THRU 'Z' 'a' THRU 'z'.
       01  result          pic s9.
       procedure division using a b result.           
           EVALUATE TRUE ALSO TRUE
               WHEN a-upper ALSO b-upper
               WHEN a-lower ALSO b-lower
                   MOVE 1 TO result
               WHEN a-alpha ALSO b-alpha
                   MOVE 0 TO RESULT
               WHEN OTHER
                   MOVE -1 TO result
           END-EVALUATE.
           goback.
       end program SameCase.
__________________________
       identification division.
       program-id. SameCase.
      
       data division.
       linkage section.
       01  a pic x.
       01  b pic x.
       01  result          pic s9.
       procedure division using a b result.           
      
       evaluate true
      
       when a is not alphabetic or b is not alphabetic
       move -1 to result
      
       when a = space or b = space
       move -1 to result
      
       when Function Upper-case(a) = a and Function Upper-case(b) = b 
       move 1 to result
      
       when Function Lower-case(a) = a and Function Lower-case(b) = b
       move 1 to result
      
       when Function Upper-case(a) = a and Function Upper-case(b) <> b
       move 0 to result
      
       when Function Lower-case(a) = a and Function Lower-case(b) <> b
       move 0 to result
           
       when other move -1 to result
      
       end-evaluate

           goback.
       end program SameCase.
__________________________
       IDENTIFICATION DIVISION.
       PROGRAM-ID. SameCase.
       DATA DIVISION.
       LINKAGE SECTION.
       01  A           PIC X.
           88  A-LW             VALUE 'a' THRU 'z'.
           88  A-UP             VALUE 'A' THRU 'Z'.
       01  B           PIC X.
           88  B-LW             VALUE 'a' THRU 'z'.
           88  B-UP             VALUE 'A' THRU 'Z'.
       01  RESULT      PIC S9.
       PROCEDURE DIVISION USING A B RESULT.
           EVALUATE  TRUE
               WHEN (A-LW AND B-LW) OR (A-UP AND B-UP)  SET RESULT TO 1
               WHEN (A-LW AND B-UP) OR (A-UP AND B-LW)  SET RESULT TO 0
               WHEN  OTHER                              SET RESULT TO -1
           END-EVALUATE.
       END PROGRAM SameCase.
__________________________
       identification division.
       program-id. SameCase.
       
       environment division.
       configuration section.
       repository. function all intrinsic.
      
       data division.
       linkage section.
       01  a pic x.
       01  b pic x.
       01  result          pic s9.
       procedure division using a b result.
           evaluate true
              when lower-case(a) = upper-case(a) or 
                   lower-case(b) = upper-case(b)
                  move -1 to result
              when lower-case(a) = a and lower-case(b) = b or
                   upper-case(a) = a and upper-case(b) = b
                  move 1 to result
              when other
                  move 0 to result
           end-evaluate.
       end program SameCase.
__________________________
       identification division.
       program-id. SameCase.
      
       data division.
       local-storage section.
       01 l constant 'abcdefghijklmnopqrstuvwxyz'.
       01 u constant 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.
       01 c pic 9.
       01 d pic 9.
       01 e pic 9.
       01 f pic 9.
       linkage section.
       01  a pic x.
       01  b pic x.
       01  result   pic s9 sign leading.
       procedure division using a b result.
      
           inspect l tallying c for all a
           inspect l tallying d for all b
           inspect u tallying e for all a
           inspect u tallying f for all b
           if c + d + e + f = 2
              if c = d
                 move 1 to result
              else
                 move 0 to result
              end-if
           else
              move -1 to result
           end-if

           goback.
       end program SameCase.
