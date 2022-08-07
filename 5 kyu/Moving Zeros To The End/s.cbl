52597aa56021e91c93000cb0
      
      
       identification division.
       program-id. move-zeros.
       data division.
      
       linkage section.
       01  arr.
           05 arr-length   pic 9(2).
           05 xs           pic 9(3) occurs 0 to 20 times 
                                    depending on arr-length
                                    indexed by i j.
       01  result.
           05 res-length   pic 9(2).
           05 res          pic 9(3) occurs 0 to 20 times 
                                    depending on res-length.
       procedure division using arr result.
           move arr-length to res-length
           set j to 1
      * result is initialized by tests
           perform varying i from 1 until i > arr-length
              if xs(i) <> 0
                  move xs(i) to res(j)
                  set j up by 1
              end-if
           end-perform
           goback.
       end program move-zeros.
_____________________________
       IDENTIFICATION DIVISION.
       PROGRAM-ID. move-zeros.
       DATA DIVISION.
       LINKAGE SECTION.
       01  ARR.
           05 ARR-LEN    PIC 9(2).
           05 XS         PIC 9(3) OCCURS 20 DEPENDING ARR-LEN INDEXED I.
       01  RESULT.
           05 RES-LEN    PIC 9(2).
           05 RES        PIC 9(3) OCCURS 20.

       PROCEDURE DIVISION USING ARR RESULT.
           PERFORM VARYING I FROM 1 UNTIL I > ARR-LEN
               IF  XS(I) NOT = 0
                   ADD  1      TO RES-LEN
                   MOVE XS(I)  TO RES(RES-LEN)
               END-IF
           END-PERFORM
           MOVE ARR-LEN  TO RES-LEN.
       END PROGRAM move-zeros.
_____________________________
       identification division.
       program-id. move-zeros.
       data division.
      
       linkage section.
       01  arr.
             05 arr-length   pic 9(2).
           05 xs           pic 9(3) occurs 0 to 20 times 
                                  depending on arr-length indexed by i.
       01  result.
           05 res-length   pic 9(2).
           05 res           pic 9(3) occurs 0 to 20 times 
                                  depending on res-length indexed by j.
       procedure division using arr result.
      
        move 1 to i
        move 1 to j
      
        move arr-length to res-length
        perform varying i from 1 by 1 until i > arr-length
          if xs(i) <> '000' then
            move xs(i) to res(j)
            compute j = j + 1            
          end-if
        end-perform
      
           goback.
       end program move-zeros.
_____________________________
       identification division.
       program-id. move-zeros.
       author. "ejini战神".
       data division.
       local-storage section.
       01  m               pic 9(2).
       linkage section.
       01  arr.
           05 arr-length   pic 9(2).
           05 xs           pic 9(3) occurs 0 to 20 times 
                                    depending on arr-length
                                    indexed by i.
       01  result.
           05 res-length   pic 9(2).
           05 res          pic 9(3) occurs 0 to 20 times 
                                    depending on res-length.
       procedure division using arr result.
           initialize m res-length
           perform varying i from 1 by 1 until i > arr-length
               if xs(i) = 0 then
                   add 1 to m
               end-if
               if xs(i) <> 0 then
                   add 1 to res-length
                   move xs(i) to res(res-length)
               end-if
           end-perform
           perform until m = 0 
               add 1 to res-length
               move 0 to res(res-length)
               subtract 1 from m
           end-perform.
       end program move-zeros.
      
