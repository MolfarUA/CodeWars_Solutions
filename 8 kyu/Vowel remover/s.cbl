5547929140907378f9000039
      
      
       IDENTIFICATION DIVISION.
       PROGRAM-ID. shortcut.
       ENVIRONMENT DIVISION.
       CONFIGURATION SECTION.
       SPECIAL-NAMES.
       CLASS VOWEL IS 'a' 'e' 'i' 'o' 'u'.
       DATA DIVISION.
       LINKAGE SECTION.
       01  STR.
           05 STR-LEN           PIC  9(02).
           05 STR-CHR           PIC  X(80).
       01  RESULT.
           05 RESULT-LEN        PIC  9(02).
           05 RESULT-CHR        PIC  X(80).
       PROCEDURE DIVISION USING STR RESULT.
           INITIALIZE RESULT
           PERFORM VARYING TALLY FROM 1 BY 1 UNTIL TALLY > STR-LEN
               IF  STR-CHR(TALLY:1) IS NOT VOWEL
                   ADD  1                 TO RESULT-LEN
                   MOVE STR-CHR(TALLY:1)  TO RESULT-CHR(RESULT-LEN:1)
               END-IF          
           END-PERFORM.
       END PROGRAM shortcut.
_____________________________
       identification division.
       program-id. shortcut.
      
       data division.
       local-storage section.
       77 chr         pic x.
          88 is-vowel  value 'a' 'e' 'i' 'o' 'u'.
      
       linkage section.
       01  str.
           05 len      pic 99.
           05 chars.
              10 char_tab    pic x occurs 0 to 80 times 
                                   depending on len in str
                                   indexed by i.
       01  result.
           05 len      pic 99.
           05 chars.
              10 char_tab    pic x occurs 0 to 80 times 
                                   depending on len in str
                                   indexed by j.
       procedure division using str result.
          initialize result
          set j to 0
          perform varying i from 1 until i > len in str
             move char_tab in str(i) to chr
             if not is-vowel then
                set j up by 1
                move chr to chars in result(j:1)
             end-if
          end-perform      
          set len in result to j
          goback.
       end program shortcut.
