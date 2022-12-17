56a1c074f87bc2201200002e
      
      
       identification division.
       program-id. Smaller.
       data division.
      
       linkage section.
       01  arr.
           05 l     pic 9(2).
           05 xs            pic s9(4) occurs 50 times 
                                      depending on l
                                      indexed by i j.
       01  result.
           05 resLength     pic 9(2).
           05 res           pic 9(2) occurs 50 times 
                                     depending on resLength.
      
       procedure division using arr result.
      
          initialize result
      
          set resLength to l
      
          perform varying i from 1 until i = l
          after   j from function abs(i + 1) until j > l
            if xs(j) < xs(i) add 1 to res(i) end-if
          end-perform
      
          goback.
       end program Smaller.
____________________________
       IDENTIFICATION DIVISION.
       PROGRAM-ID. Smaller.
       DATA DIVISION.
       LINKAGE SECTION.
       01  ARR.
           05 ARR-LEN   PIC  9(2).
           05 XS        PIC S9(4) OCCURS 50 DEPENDING ARR-LEN INDEXED I.
       01  RESULT.
           05 RES-LEN   PIC  9(2).
           05 RES       PIC  9(2) OCCURS 50 DEPENDING RES-LEN INDEXED J.

       PROCEDURE DIVISION USING ARR RESULT.
          INITIALIZE RESULT
          PERFORM VARYING I FROM 1 UNTIL I > ARR-LEN
                  AFTER   J FROM I UNTIL J > ARR-LEN
              IF  XS(I) > XS(J)
                  ADD 1  TO RES(I)
              END-IF
          END-PERFORM
          MOVE ARR-LEN  TO RES-LEN.
       END PROGRAM Smaller.
