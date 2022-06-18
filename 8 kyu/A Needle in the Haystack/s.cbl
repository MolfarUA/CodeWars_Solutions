       identification division.
       program-id. FindNeedle.
       author. "ejini战神".
       data division.
       local-storage section.      
       01  n                 pic z(2)9.
       linkage section.
       01  arr.
           05 arr-length     pic 9(3).
           05 xs             pic x(40) occurs 1 to 300 times 
                                      depending on arr-length
                                      indexed by i.
       01  result.
           05 res-length     pic 9(2).
           05 res.            
              07  pic x      occurs 30 to 32 times 
                             depending on res-length
                             indexed by j.
      
       procedure division using arr result.  
          initialize result
          perform varying i from 1 by 1 until i > arr-length
              if xs(i) = "needle" then 
                  exit perform
              end-if
          end-perform                   
          move 32 to res-length
          set j to 1
          move i to n
          string "found the needle at position " function trim(n) 
          into res pointer j       
          compute res-length = j - 1.
       end program FindNeedle.
________________________
       IDENTIFICATION DIVISION.
       PROGRAM-ID. FindNeedle.
       DATA DIVISION.
       LOCAL-STORAGE SECTION.
       01  I            PIC 9(03).
       01  OUT.
           05 OUT-LEN   PIC 9(02) VALUE 30.
           05 FILLER    PIC X(29) VALUE 'found the needle at position '.
           05 OUT-POS   PIC X(03).

       LINKAGE SECTION.
       01  ARR.
           05 ARR-LEN   PIC 9(03).
           05 XS        PIC X(40) OCCURS 300 DEPENDING ARR-LEN.
       01  RESULT       PIC X(34).

       PROCEDURE DIVISION USING ARR RESULT.
           PERFORM VARYING I FROM 1 UNTIL XS(I) = 'needle'  END-PERFORM
           ADD  FUNCTION LOG10(I)          TO OUT-LEN
           MOVE I(3 - FUNCTION LOG10(I):)  TO OUT-POS
           MOVE OUT                        TO RESULT.
       END PROGRAM FindNeedle.
________________________
       identification division.
       program-id. FindNeedle.
       data division.
       local-storage section.
       01  n                 pic z(2)9.
      
       linkage section.
       01  arr.
           05 arr-length     pic 9(3).
           05 xs             pic x(40) occurs 1 to 300 times 
                                      depending on arr-length indexed i.
       01  result.
           05 res-length     pic 9(2).
           05 s.
              07 pic x       occurs 30 to 32 times 
                             depending on res-length indexed j.
      
       procedure division using arr result.
      
          set i to 1
          perform test before until xs(i) = 'needle'
              add 1 to i
          end-perform
      
          initialize result
          move 32 to res-length
          set j to 1
          move i to n
          string 'found the needle at position ' function trim(n)
          into s pointer j
      
          compute res-length = j - 1
          
          goback.
       end program FindNeedle.
________________________
       identification division.
       program-id. FindNeedle.
       data division.
       working-storage section.
       77 needlePos          pic zz9.
       77 ptr                usage is index.

       linkage section.
       01  arr.
           05 arr-length     pic 9(3).
           05 xs             pic x(40) occurs 1 to 300 times 
                                      depending on arr-length
                                      indexed by i.
       01  result.
           05 res-length     pic 9(2).
           05 res-Str.
              10 res            pic x occurs 30 to 32 times 
                                      depending on res-length.
      
       procedure division using arr result.
          move 32 to res-length
          set i to 1
          search xs
             at end continue
             when xs(i) = 'needle' move i to needlePos
          end-search
          set ptr to 1
          string 'found the needle at position ' 
                 function trim(NeedlePos)
            into res-Str
            with pointer ptr
          end-string
          subtract 1 from ptr giving res-Length
          goback.
       end program FindNeedle.
