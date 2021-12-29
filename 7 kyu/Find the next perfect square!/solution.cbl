       identification division.
       program-id. NEXT-SQUARE.
       data division.
       local-storage section.
       01 isqrt       PIC 9(10).
       linkage section.
       01 n           PIC 9(20).
       01 result      PIC s9(20) sign leading.
       procedure division using n result.
      
          compute isqrt = function sqrt(n)

          if n = isqrt ** 2
            compute result = (isqrt + 1) ** 2
          else
            move -1 to result
          end-if
      
          goback.
       end program NEXT-SQUARE.
      
_______________________________________
       identification division.
       program-id. NEXT-SQUARE.
       data division.
       linkage section.
       01 n           PIC 9(20).
       01 result      PIC s9(20) sign leading.
       procedure division using n result.
          compute result = n ** 0.5
          if result * result = n
              compute result = (result + 1) ** 2
          else
              compute result = -1
          end-if.
       end program NEXT-SQUARE.
      
_______________________________________
       identification division.
       program-id. NEXT-SQUARE.
       data division.
       local-storage section.
       01 a           PIC 9(10).
       linkage section.
       01 n           PIC 9(20).
       01 result      PIC s9(20) sign leading.
       procedure division using n result.
          compute a = function sqrt(n),
          move -1 to result,
          if n = a * a
            compute result = (a + 1) ** 2
          end-if,
          goback.
       end program NEXT-SQUARE.
      
