57a5c31ce298a7e6b7000334
      
      
       identification division.
       program-id. BinToDec.
      
       data division.
       working-storage section.
       77 i         usage is index.
      
       linkage section.
       01 bin         pic x(127).
       01 result      pic 9(38).
      
       procedure division using bin result.
          initialize result
          perform varying i from 1 until i > function length(bin) 
                                      or bin(i:1) = space
             multiply 2 by result
             if bin(i:1) = '1' then
                add 1 to result
             end-if
          end-perform
          goback.
       end program BinToDec.
_________________________
       identification division.
       program-id. BinToDec.
      
       data division.
       working-storage section.
       01 i           usage index.
       01 d           pic 9.
       linkage section.
       01 bin         pic x(127).
       01 result      pic 9(38).
      
       procedure division using bin result.
          initialize result
          perform varying i from 1 until i > 127 or bin(i:1) = space
              move bin(i:1) to d
              compute result = 2 * result + d
          end-perform.
       end program BinToDec.
_________________________
       identification division.
       program-id. BinToDec.
       data division.
       linkage section.
       01 bin.
          03 c        pic x occurs 127 indexed i.
       01 result      pic 9(38).
       procedure division using bin result.
          initialize result
          perform varying i from 1 
              until i > length of function trim(bin)
            compute result = 2 * result + function numval(c(i))
          end-perform.
       end program BinToDec.
