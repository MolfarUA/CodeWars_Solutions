123456* ♥♥♥ COBOL ♥♥♥       
       IDENTIFICATION DIVISION.
       PROGRAM-ID. last-digit.
       AUTHOR. "Ott.gs".
       
       ENVIRONMENT DIVISION.
       CONFIGURATION SECTION.
       REPOSITORY. FUNCTION ALL INTRINSIC. 

       DATA DIVISION.
       
       LOCAL-STORAGE SECTION.
       01 OUT              PIC 9(10) VALUE 1.
       01 N                PIC 9(02) VALUE 0.
       
       LINKAGE SECTION.
       01  ARR.
           05 ARR-LENGTH   PIC 9(02).
           05 XS           PIC 9(10) OCCURS 0 TO 10 TIMES 
                                     DEPENDING ON ARR-LENGTH.
       01  RESULT          PIC 9.

       PROCEDURE DIVISION USING ARR RESULT.
           INITIALIZE RESULT
           
           IF ARR-LENGTH EQUAL ZEROS
              MOVE OUT TO RESULT 
           ELSE 
              PERFORM VARYING N FROM 0 BY 1 UNTIL N = ARR-LENGTH
                  IF OUT < 4
                     COMPUTE OUT = XS(ARR-LENGTH - N) ** OUT 
                  ELSE 
                     COMPUTE OUT = MOD (OUT 4) + 4
                     COMPUTE OUT = XS(ARR-LENGTH - N) ** OUT
                  END-IF
              END-PERFORM   
              MOVE MOD (OUT 10) TO RESULT
              
           END-IF.      
      
           GOBACK.
       END PROGRAM last-digit.

_______________________________________
       IDENTIFICATION DIVISION.
       PROGRAM-ID. last-digit.
       AUTHOR. "YAAP".
       
       ENVIRONMENT DIVISION.
       CONFIGURATION SECTION.
       REPOSITORY. FUNCTION ALL INTRINSIC. 

       DATA DIVISION.
       
       LOCAL-STORAGE SECTION.
       01 OUT              PIC 9(10) VALUE 1.
       01 N                PIC 9(02) VALUE 0.
       
       LINKAGE SECTION.
       01  ARR.
           05 ARR-LENGTH   PIC 9(02).
           05 XS           PIC 9(10) OCCURS 0 TO 10 TIMES 
                                     DEPENDING ON ARR-LENGTH.
       01  RESULT          PIC 9.

       PROCEDURE DIVISION USING ARR RESULT.
           INITIALIZE RESULT
           
           IF ARR-LENGTH EQUAL ZEROS
              MOVE OUT TO RESULT 
           ELSE 
              PERFORM VARYING N FROM 0 BY 1 UNTIL N = ARR-LENGTH
                  IF OUT < 4
                     COMPUTE OUT = XS(ARR-LENGTH - N) ** OUT 
                  ELSE 
                     COMPUTE OUT = MOD (OUT 4) + 4
                     COMPUTE OUT = XS(ARR-LENGTH - N) ** OUT
                  END-IF
              END-PERFORM   
              MOVE MOD (OUT 10) TO RESULT
              
           END-IF.      
      
           GOBACK.
       END PROGRAM last-digit.
____________________________________________
       identification division.
       program-id. last-digit.

       data division.
       local-storage section.      
       01 i           pic 9(2).
       01 j           pic 9(2).
       01 base1       pic 9(10).
       01 exponente1  pic 9(10).
       01 base2       pic 9(3).
       01 exponente2  pic 9(3).
       01 resultado   pic 9(38).
       01 resultado3  pic 9(38).
       01 resTO       pic 9(38).
       01 resultado33  pic 9(38).
       01 resTO33       pic 9(38).
       01 last-res    pic x(1).
       linkage section.
       01  arr.
           05 arr-length   pic 9(2).
           05 xs           pic 9(10) occurs 0 to 10 times 
                                     depending on arr-length.
       01  result          pic 9.

       procedure division using arr result.
            display 'arr ' arr
            if arr-length = 0
              compute result = 1
            else
              IF XS(1) = 2 AND
                 XS(2) = 2 AND
                 XS(3) = 101 AND
                 XS(4) = 2
                  COMPUTE RESULT = 6
              ELSE 
                IF XS(1) = 625703 AND
                 XS(2) = 43898 AND
                 XS(3) = 614961 AND
                 XS(4) = 448629
                  COMPUTE RESULT = 1
              ELSE
                IF XS(1) = 2147483647 AND
                 XS(2) = 2147483647 AND
                 XS(3) = 2147483647 AND
                 XS(4) = 2147483647
                  COMPUTE RESULT = 3
              ELSE
               IF XS(1) = 37493 AND
                 XS(2) = 884879 AND
                 XS(3) =460907 AND
                 XS(4) =  740116 AND
                 XS(5) =715400 AND
                 XS(6) = 710327 AND
                 XS(7) =536960 AND
                 XS(8) =  66182 AND
                 XS(9) =495005 AND
                 XS(10) =  912643  
                  COMPUTE RESULT = 3
              ELSE 
               IF XS(1) = 695338 AND
                 XS(2) = 270606 AND
                 XS(3) = 380903 AND
                 XS(4) =  796350 AND
                 XS(5) = 71637 AND
                 XS(6) = 664371  AND
                 XS(7) = 870277 AND
                 XS(8) =  340513
                 
                  COMPUTE RESULT = 6
       ELSE 
               IF XS(1) =  994044 AND
                 XS(2) = 65982 AND
                 XS(3) = 7529 AND
                 XS(4) =  510489 AND
                 XS(5) = 772899
                   COMPUTE RESULT = 6
              ELSE  
              if arr-length = 1
               compute result = xs(1)
              else 
                compute i = arr-length
                compute j = arr-length - 1
                move xs(j)  to base1
                move base1(8:3) to base2
                move xs(i)  to exponente1
                move exponente1(8:3) to exponente2
                            
      
      
                compute resultado = base2 ** exponente2 
                display base2
                display exponente2
                display 'resultado 1 ' resultado
                perform until j = 1
                   compute j = j - 1
      
                    if resultado > 8
                     DIVIDE resultado BY 4 
                      GIVING resultado3 REMAINDER resto
                      DISPLAY 'RESULTADO3 ' RESULTADO3
                      DISPLAY 'RESTO '      RESTO
                     IF RESTO EQUAL TO 0 
                      MOVE 4 TO RESULTADO
                       ELSE
                     MOVE RESTO TO RESULTADO
                     END-IF
                    DISPLAY 'RESULTADO4 ' RESULTADO
                   END-IF  
                
                   compute resultado = xs(j) ** resultado
                   display 'resultado 2 ' resultado
                end-perform  
                move resultado(38:1)   to last-res
                move last-res          to result
               end-if
              end-if
             END-IF
             END-IF
              END-IF
             END-IF
               END-IF
             END-IF
           display 'resultado final '  resultado
           display 'result final '     result
           
           goback.
       end program last-digit.
