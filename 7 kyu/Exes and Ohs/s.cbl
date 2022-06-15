       identification division.
       program-id. Xo.
      
       data division.
       local-storage section.
       01 x    pic 999.
       01 o    pic 999.

       linkage section.
       01 s           pic a(100).
       01 result      pic 9.
      
       procedure division using s result.
          inspect s tallying x for all 'x' x for all 'X'
                             o for all 'o' o for all 'O'
          if x = o then move 1 to result else move 0 to result.
       end program Xo.
__________________________________
       identification division.
       program-id. Xo.
       data division.
       local-storage section.
       01 x           pic 9(2).
       01 o           pic 9(2).
       linkage section.
       01 s           pic x(100).
       01 result      pic 9.
       procedure division using s result.
          initialize result
          inspect function lower-case(s) tallying x for all 'x'
          inspect function lower-case(s) tallying o for all 'o'
          if x = o then move 1 to result end-if.
       end program Xo.
__________________________________
       identification division.
       program-id. Xo.
      
       data division.
       local-storage section.
       01 a           pic 9(2).
       01 b           pic 9(2).
      
       linkage section.
       01 s           pic x(100).
       01 result      pic 9.
      
       procedure division using s result.
      
          initialize result
      
          inspect function lower-case(s) tallying a for all 'x'
          inspect function lower-case(s) tallying b for all 'o'
          if a = b move 1 to result end-if
      
          goback.
       end program Xo.
